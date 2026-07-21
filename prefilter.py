import yfinance as yf
import pandas as pd
import time
import logging
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from config import (
    STOCK_LIST, BATCH_SIZE, SLEEP_BETWEEN_BATCHES,
    MIN_VOLUME, MIN_TRANSACTION_VALUE, HIGH_PRICE_THRESHOLD
)

logger = logging.getLogger(__name__)

def fetch_batch_data(tickers: List[str], period: str = "1mo") -> pd.DataFrame:
    """Fetch data batch untuk 1 bulan (cek volume & harga)"""
    try:
        data = yf.download(
            tickers,
            period=period,
            group_by='ticker',
            threads=True,
            progress=False
        )
        return data
    except Exception as e:
        logger.error(f"Batch fetch error: {e}")
        return pd.DataFrame()

def prefilter_stocks(capital: float = 1_000_000) -> Tuple[List[str], List[Dict]]:
    """
    Tahap 1: Filter saham zombie & label harga.
    Return: (list_ticker_lolos, list_info_saham)
    """
    total = len(STOCK_LIST)
    logger.info(f"[PREFILTER] Memulai filter {total} saham...")
    
    passed_tickers = []
    stock_info = []  # simpan metadata
    
    for i in range(0, total, BATCH_SIZE):
        batch = STOCK_LIST[i:i+BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        total_batches = (total // BATCH_SIZE) + 1
        logger.info(f"[PREFILTER] Batch {batch_num}/{total_batches} ({len(batch)} saham)")
        
        data = fetch_batch_data(batch, "1mo")
        
        if data.empty:
            logger.warning(f"[PREFILTER] Batch {batch_num} kosong, sleep {SLEEP_BETWEEN_BATCHES}s")
            time.sleep(SLEEP_BETWEEN_BATCHES)
            continue
        
        for ticker in batch:
            try:
                if ticker in data.columns.levels[1]:
                    df = data.xs(ticker, level=1, axis=1)
                else:
                    df = yf.download(ticker, period="1mo", progress=False)
                
                if df.empty or len(df) < 5:
                    continue
                
                # Hitung rata-rata volume & nilai transaksi
                avg_volume = df['Volume'].rolling(20).mean().iloc[-1]
                avg_price = df['Close'].mean()
                avg_value = avg_volume * avg_price  # estimasi nilai transaksi harian
                
                # Cek zombie: volume < min atau nilai < min
                if avg_volume < MIN_VOLUME or avg_value < MIN_TRANSACTION_VALUE:
                    continue
                
                # Ambil harga terbaru
                last_price = df['Close'].iloc[-1]
                
                # Label High/Low Price
                price_label = "High Price" if last_price >= HIGH_PRICE_THRESHOLD else "Low Price"
                price_emoji = "🏷️" if last_price >= HIGH_PRICE_THRESHOLD else "📉"
                
                passed_tickers.append(ticker)
                stock_info.append({
                    'ticker': ticker.replace('.JK', ''),
                    'last_price': last_price,
                    'avg_volume': avg_volume,
                    'avg_value': avg_value,
                    'price_label': f"{price_emoji} {price_label} (Rp{last_price:,.0f})"
                })
                
            except Exception as e:
                logger.debug(f"[PREFILTER] Error {ticker}: {e}")
                continue
        
        time.sleep(SLEEP_BETWEEN_BATCHES)
    
    logger.info(f"[PREFILTER] Selesai. Lolos: {len(passed_tickers)} saham dari {total}")
    return passed_tickers, stock_info
