import pandas as pd
import numpy as np
from typing import Dict, List, Optional

def detect_double_bottom(df: pd.DataFrame, lookback: int = 30) -> bool:
    """Double Bottom: 2 titik rendah dalam 30 hari, selisih < 2%"""
    if len(df) < lookback:
        return False
    recent = df.tail(lookback)
    lows = recent['Low']
    # Cari 2 titik terendah
    min1 = lows.min()
    idx1 = lows.idxmin()
    # Cari titik terendah kedua setelah idx1
    second_low = lows[idx1:].min() if idx1 < lows.index[-1] else None
    if second_low is None:
        return False
    diff = abs(min1 - second_low) / min1
    return diff < 0.02  # < 2% selisih

def detect_cup_handle(df: pd.DataFrame, lookback: int = 60) -> bool:
    """Cup & Handle: bentuk U diikuti konsolidasi kecil"""
    if len(df) < lookback:
        return False
    recent = df.tail(lookback)
    # Cek bentuk U: titik tengah (30 hari) lebih rendah dari ujung
    mid = int(lookback/2)
    left = recent['Close'].iloc[0]
    right = recent['Close'].iloc[-1]
    mid_price = recent['Close'].iloc[mid]
    
    if mid_price < left * 0.95 and mid_price < right * 0.95:
        # Cek handle: konsolidasi di 10 hari terakhir
        handle = recent.tail(10)
        if handle['Close'].max() - handle['Close'].min() < 0.03 * handle['Close'].mean():
            return True
    return False

def detect_breakout(df: pd.DataFrame, lookback: int = 20) -> bool:
    """Breakout: harga tutup > resistance 20-hari & volume > 1.5x avg"""
    if len(df) < lookback + 1:
        return False
    recent = df.tail(lookback + 1)
    resistance = recent['High'].iloc[:-1].max()
    current_close = recent['Close'].iloc[-1]
    avg_volume = recent['Volume'].iloc[:-1].mean()
    current_volume = recent['Volume'].iloc[-1]
    
    if current_close > resistance and current_volume > avg_volume * 1.5:
        return True
    return False

def detect_head_shoulders(df: pd.DataFrame, lookback: int = 60) -> bool:
    """Head & Shoulders: 3 puncak, tengah tertinggi"""
    if len(df) < lookback:
        return False
    recent = df.tail(lookback)
    # Cari puncak lokal (sederhana)
    highs = recent['High']
    peaks = []
    for i in range(5, len(highs)-5):
        if highs.iloc[i] > highs.iloc[i-5] and highs.iloc[i] > highs.iloc[i+5]:
            peaks.append((i, highs.iloc[i]))
    if len(peaks) < 3:
        return False
    # Ambil 3 puncak terakhir
    peaks = peaks[-3:]
    if peaks[1][1] > peaks[0][1] and peaks[1][1] > peaks[2][1]:
        return True
    return False

def detect_bullish_flag(df: pd.DataFrame, lookback: int = 30) -> bool:
    """Bullish Flag: kenaikan tajam diikuti konsolidasi miring turun"""
    if len(df) < lookback:
        return False
    recent = df.tail(lookback)
    # Cek kenaikan tajam di 10 hari pertama
    first_10 = recent.iloc[:10]
    if first_10['Close'].iloc[-1] > first_10['Close'].iloc[0] * 1.10:
        # Cek konsolidasi di 20 hari terakhir (flag)
        flag = recent.iloc[10:]
        if len(flag) > 5:
            slope = (flag['Close'].iloc[-1] - flag['Close'].iloc[0]) / len(flag)
            if slope < 0:  # miring turun
                return True
    return False

def detect_all_patterns(df: pd.DataFrame) -> List[str]:
    """Deteksi semua pola, return list pola yang terdeteksi"""
    patterns = []
    if detect_double_bottom(df):
        patterns.append("Double Bottom 🔄")
    if detect_cup_handle(df):
        patterns.append("Cup & Handle ☕")
    if detect_breakout(df):
        patterns.append("Breakout 🚀")
    if detect_head_shoulders(df):
        patterns.append("Head & Shoulders ⚠️")
    if detect_bullish_flag(df):
        patterns.append("Bullish Flag 🚩")
    return patterns