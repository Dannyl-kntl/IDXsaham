import pandas as pd
import numpy as np
from config import (
    CAPITAL, RISK_PER_TRADE, ATR_PERIOD,
    STOP_LOSS_ATR_MULTIPLIER, TAKE_PROFIT_1_ATR_MULTIPLIER,
    TAKE_PROFIT_2_ATR_MULTIPLIER
)

def calculate_atr(df: pd.DataFrame, period: int = ATR_PERIOD) -> float:
    high = df['High']
    low = df['Low']
    close = df['Close']
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean().iloc[-1]
    return atr

def get_trading_levels(df: pd.DataFrame, indicators: dict) -> dict:
    current_price = indicators['current_price']
    atr = calculate_atr(df)
    
    # Entry: default di harga sekarang, atau di MA50 jika lebih rendah (support)
    entry = current_price
    if indicators.get('ma50') and indicators['ma50'] < current_price:
        entry = indicators['ma50']  # entry di support MA50
    
    # Stop Loss & Take Profit
    stop_loss = entry - (atr * STOP_LOSS_ATR_MULTIPLIER)
    take_profit_1 = entry + (atr * TAKE_PROFIT_1_ATR_MULTIPLIER)
    take_profit_2 = entry + (atr * TAKE_PROFIT_2_ATR_MULTIPLIER)
    
    # Position Sizing
    risk_amount = CAPITAL * RISK_PER_TRADE
    risk_per_share = abs(entry - stop_loss)
    position_size = int(risk_amount / risk_per_share) if risk_per_share > 0 else 0
    
    # Risk-Reward Ratio
    rr_ratio = abs(take_profit_1 - entry) / abs(entry - stop_loss) if abs(entry - stop_loss) > 0 else 0
    
    return {
        'entry': round(entry, 0),
        'stop_loss': round(stop_loss, 0),
        'take_profit_1': round(take_profit_1, 0),
        'take_profit_2': round(take_profit_2, 0),
        'atr': round(atr, 0),
        'position_size': position_size,
        'risk_reward': round(rr_ratio, 2),
        'risk_amount': round(risk_amount, 0),
    }
