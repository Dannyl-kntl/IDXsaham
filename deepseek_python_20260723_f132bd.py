import requests
import yfinance as yf
import pandas as pd
from config import ITICK_API_KEY, ITICK_BASE_URL, USE_YFINANCE_FALLBACK

class IDXDataFetcher:
    def __init__(self):
        self.itick_key = ITICK_API_KEY
        self.use_yfinance = USE_YFINANCE_FALLBACK
    
    def get_stock_info(self, ticker):
        """Ambil data fundamental saham"""
        try:
            # Coba iTick dulu
            if self.itick_key:
                data = self._fetch_from_itick(ticker)
                if data:
                    return data
            
            # Fallback ke Yahoo Finance
            if self.use_yfinance:
                return self._fetch_from_yfinance(ticker)
            
            return None
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            return None
    
    def _fetch_from_itick(self, ticker):
        """Ambil data dari iTick API"""
        try:
            # Quote real-time
            url = f"{ITICK_BASE_URL}/stock/quote"
            params = {"region": "ID", "code": ticker}
            headers = {"token": self.itick_key}
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get("code") == 0:
                    quote = data.get("data", {})
                    return {
                        "ticker": ticker,
                        "name": quote.get("n", ticker),
                        "price": quote.get("ld", 0),
                        "change": quote.get("chp", 0),
                        "volume": quote.get("v", 0),
                    }
            return None
        except:
            return None
    
    def _fetch_from_yfinance(self, ticker):
        """Ambil data dari Yahoo Finance (ticker diakhiri .JK)"""
        try:
            stock = yf.Ticker(f"{ticker}.JK")
            info = stock.info
            
            # Ambil data historis untuk growth
            hist = stock.history(period="5y")
            
            return {
                "ticker": ticker,
                "name": info.get("longName", ticker),
                "price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
                "market_cap": info.get("marketCap", 0),
                "pe_ratio": info.get("trailingPE", 0),
                "pb_ratio": info.get("priceToBook", 0),
                "roe": info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else 0,
                "der": self._calculate_der(info),
                "dividend_yield": info.get("dividendYield", 0) * 100 if info.get("dividendYield") else 0,
                "payout_ratio": info.get("payoutRatio", 0) * 100 if info.get("payoutRatio") else 0,
                "revenue_growth_5y": self._calculate_growth(hist, "revenue"),
                "profit_growth_5y": self._calculate_growth(hist, "profit"),
                "sector": info.get("sector", "Unknown"),
                "volume": info.get("volume", 0),
                "avg_volume": info.get("averageVolume", 0),
                "free_float": info.get("freeFloat", 0) * 100 if info.get("freeFloat") else 0,
            }
        except Exception as e:
            print(f"YFinance error {ticker}: {e}")
            return None
    
    def _calculate_der(self, info):
        """Hitung Debt to Equity Ratio"""
        debt = info.get("totalDebt", 0)
        equity = info.get("bookValue", 0) * info.get("sharesOutstanding", 1) if info.get("bookValue") else 0
        if equity > 0:
            return debt / equity
        return 0
    
    def _calculate_growth(self, hist, metric):
        """Hitung growth 5 tahun"""
        # Simplified - dalam implementasi riil, ambil dari laporan keuangan
        # Di sini kita gunakan proksi dari data Yahoo
        return 0  # Placeholder
    
    def get_sector_avg_pe(self, sector):
        """Dapatkan rata-rata PER sektor"""
        # Data statis berdasarkan laporan sebelumnya
        sector_avg = {
            "Consumer Non-Cyclical": 15.91,
            "Basic Materials": 15.0,
            "Financial": 13.0,
            "Energy": 13.12,
            "Infrastructure": 12.0,
            "Healthcare": 18.0,
            "Technology": 20.0,
            "Property": 10.0,
            "Transportation": 11.0,
            "Others": 14.0
        }
        return sector_avg.get(sector, 14.0)