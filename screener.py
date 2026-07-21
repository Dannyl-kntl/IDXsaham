import yfinance as yf
import pandas as pd
import pandas_ta as ta
import time
import logging
from typing import List, Dict, Optional, Tuple
from config import RSI_OVERSOLD, RSI_OVERBOUGHT, MA_FAST, MA_SLOW, BB_STD
from patterns import detect_all_patterns
from risk_manager import get_trading_levels

logger = logging.getLogger(__name__)

def analyze_single_stock(ticker: str, df: pd.DataFrame) -> Optional[Dict]:
    """Analisis mendalam 6 bulan untuk 1 saham"""
    if df.empty or len(df) < 50:
        return None
    
    close = df['Close']
    high = df['High']
    low = df['Low']
    volume = df['Volume']
    
    # MA
    ma50 = close.rolling(50).mean().iloc[-1]
    ma100 = close.rolling(100).mean().iloc[-1]
    ma200 = close.rolling(200).mean().iloc[-1]
    
    # RSI
    rsi = ta.rsi(close, length=14).iloc[-1]
    rsi = rsi if not pd.isna(rsi) else 50
    
    # MACD
    macd = ta.macd(close, fast=12, slow=26, signal=9)
    macd_diff = macd['MACD_12_26_9'].iloc[-1] - macd['MACDs_12_26_9'].iloc[-1] if 'MACD_12_26_9' in macd else 0
    
    # Bollinger Bands
    bb = ta.bbands(close, length=20, std=BB_STD)
    bb_lower = bb['BBL_20_2.0'].iloc[-1] if 'BBL_20_2.0' in bb else close.iloc[-1]
    bb_upper = bb['BBU_20_2.0'].iloc[-1] if 'BBU_20_2.0' in bb else close.iloc[-1]
    
    # Volume
    avg_volume = volume.rolling(20).mean().iloc[-1]
    volume_ratio = volume.iloc[-1] / avg_volume if avg_volume > 0 else 0
    
    current_price = close.iloc[-1]
    price_change = ((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] * 100) if len(close) > 1 else 0
    
    # Support/Resistance (20 hari)
    recent_high = high.tail(20).max()
    recent_low = low.tail(20).min()
    
    indicators = {
        'current_price': current_price,
        'ma50': ma50,
        'ma200': ma200,
        'rsi': rsi,
        'macd_diff': macd_diff,
        'bb_lower': bb_lower,
        'bb_upper': bb_upper,
        'volume_ratio': volume_ratio,
        'price_change': price_change,
        'recent_high': recent_high,
        'recent_low': recent_low,
        'avg_volume': avg_volume,
        'current_volume': volume.iloc[-1],
    }
    
    # === SCORING ===
    signals = []
    score = 0
    
    # RSI
    if rsi < RSI_OVERSOLD:
        signals.append(f"RSI {rsi:.0f} Oversold")
        score += 2
    elif rsi > RSI_OVERBOUGHT:
        signals.append(f"RSI {rsi:.0f} Overbought")
        score -= 1
    
    # MA Crossover
    if ma50 and ma200:
        if ma50 > ma200:
            signals.append("Golden Cross")
            score += 2
        else:
            signals.append("Death Cross")
            score -= 1
    
    # MACD
    if macd_diff > 0:
        signals.append("MACD Bullish")
        score += 2
    else:
        signals.append("MACD Bearish")
        score -= 1
    
    # Price vs MA50
    if ma50 and current_price > ma50:
        signals.append("Above MA50")
        score += 1
    else:
        signals.append("Below MA50")
        score -= 1
    
    # Bollinger
    if current_price <= bb_lower * 1.01:
        signals.append("Near Lower BB")
        score += 1
    elif current_price >= bb_upper * 0.99:
        signals.append("Near Upper BB")
        score -= 1
    
    # Volume spike
    if volume_ratio > 2.0:
        signals.append(f"Vol {volume_ratio:.1f}x avg")
        score += 1
    
    # Support/Resistance
    if current_price <= recent_low * 1.02:
        signals.append("Near Support")
        score += 1
    elif current_price >= recent_high * 0.98:
        signals.append("Near Resistance (Breakout?)")
        score += 1
    
    # === DETEKSI POLA ===
    patterns = detect_all_patterns(df)
    
    # Bonus untuk pola
    if "Breakout 🚀" in patterns:
        score += 2
        signals.append("Breakout detected!")
    if "Double Bottom 🔄" in patterns:
        score += 2
        signals.append("Double Bottom!")
    if "Bullish Flag 🚩" in patterns:
        score += 1
    
    # === TRADING LEVELS ===
    levels = get_trading_levels(df, indicators)
    
    return {
        'ticker': ticker.replace('.JK', ''),
        'price': current_price,
        'change': price_change,
        'score': score,
        'signals': signals,
        'rsi': rsi,
        'volume_ratio': volume_ratio,
        'patterns': patterns,
        'entry': levels['entry'],
        'stop_loss': levels['stop_loss'],
        'take_profit_1': levels['take_profit_1'],
        'take_profit_2': levels['take_profit_2'],
        'rr_ratio': levels['risk_reward'],
        'position_size': levels['position_size'],
        'atr': levels['atr'],
        'is_breakout': "Breakout 🚀" in patterns,
    }

def run_full_screening(tickers: List[str]) -> List[Dict]:
    """Tahap 2: Analisis mendalam untuk ticker yang lolos prefilter"""
    results = []
    total = len(tickers)
    logger.info(f"[SCREENER] Analisis mendalam {total} saham...")
    
    for i, ticker in enumerate(tickers):
        try:
            df = yf.download(ticker, period="6mo", progress=False)
            if not df.empty:
                result = analyze_single_stock(ticker, df)
                if result:
                    results.append(result)
            time.sleep(0.5)  # delay kecil antar saham
        except Exception as e:
            logger.debug(f"[SCREENER] Error {ticker}: {e}")
    
    results.sort(key=lambda x: x['score'], reverse=True)
    logger.info(f"[SCREENER] Selesai, {len(results)} saham dianalisis.")
    return results
