import pandas as pd
import numpy as np
import time  # <-- TAMBAHKAN INI
from data_fetcher import IDXDataFetcher
from config import TOP_N, MIN_ROE, MAX_DER, MIN_DIV_YIELD, IDX_TICKERS

class StockScreener:
    def __init__(self):
        self.fetcher = IDXDataFetcher()
        self.results = []
    
    def run_screening(self):
        """Jalankan screening untuk semua saham dengan jeda untuk hindari rate limit"""
        print(f"🔄 Screening {len(IDX_TICKERS)} saham IDX...")
        
        for i, ticker in enumerate(IDX_TICKERS):
            if i % 10 == 0:
                print(f"  Progress: {i}/{len(IDX_TICKERS)}")
            
            try:
                data = self.fetcher.get_stock_info(ticker)
                if not data:
                    # Jeda 1 detik meskipun data kosong
                    time.sleep(1)
                    continue
                
                # Terapkan 10 kriteria screening
                score = self._calculate_score(data)
                if score > 0:
                    data["score"] = score
                    self.results.append(data)
                
                # Jeda 1 detik ANTAR PERMINTAAN (kunci utama)
                time.sleep(1)
                
            except Exception as e:
                print(f"⚠️ Error pada {ticker}: {e}")
                print("  Menunggu 5 detik sebelum melanjutkan...")
                time.sleep(5)
                continue
        
        # Urutkan berdasarkan skor tertinggi
        self.results.sort(key=lambda x: x.get("score", 0), reverse=True)
        return self.results[:TOP_N]
    
    # Fungsi _calculate_score, format_results, get_detail, _calculate_moat, _calculate_risk
    # tetap SAMA PERSIS seperti kode yang Anda miliki, tidak perlu diubah.
    # (saya tidak menulis ulang di sini agar tidak terlalu panjang, 
    #  silakan salin dari file yang sudah ada)
