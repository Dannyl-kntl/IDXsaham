import requests
import yfinance as yf
import pandas as pd
from config import ITICK_API_KEY, ITICK_BASE_URL, USE_YFINANCE_FALLBACK

class IDXDataFetcher:
    def __init__(self):
        self.itick_key = ITICK_API_KEY
        self.use_yfinance = USE_YFINANCE_FALLBACK
        self.session = requests.Session()
    
    def get_stock_info(self, ticker):
        """Ambil data fundamental saham"""
        try:
            if self.itick_key:
                data = self._fetch_from_itick(ticker)
                if data and data.get("pe_ratio", 0) > 0:
                    # Jika iTick mengembalikan data dengan PER > 0, anggap berhasil
                    return data
                elif data:
                    # Jika iTick hanya mengembalikan harga (tanpa fundamental), lanjut ke Yahoo
                    print(f"iTick untuk {ticker} hanya data harga, fallback ke Yahoo")
            
            if self.use_yfinance:
                return self._fetch_from_yfinance(ticker)
            
            return None
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            return None
    
    def _fetch_from_itick(self, ticker):
        """Ambil data dari iTick API (Quote + Fundamental)"""
        try:
            headers = {"token": self.itick_key}
            params = {"region": "ID", "code": ticker}
            
            # 1. Ambil Harga (Quote)
            url = f"{ITICK_BASE_URL}/stock/quote"
            resp = self.session.get(url, params=params, headers=headers, timeout=10)
            if resp.status_code != 200:
                print(f"iTick quote error {ticker}: {resp.status_code}")
                return None
            data = resp.json()
            if data.get("code") != 0:
                print(f"iTick quote code error {ticker}: {data.get('code')}")
                return None
            quote = data.get("data", {})
            
            # 2. Ambil Fundamental (Statistik)
            # Coba beberapa endpoint umum iTick
            stat = {}
            endpoints = ["/stock/stat", "/stock/basic", "/stock/fundamental"]
            for endpoint in endpoints:
                try:
                    stat_url = f"{ITICK_BASE_URL}{endpoint}"
                    stat_resp = self.session.get(stat_url, params=params, headers=headers, timeout=10)
                    if stat_resp.status_code == 200:
                        stat_data = stat_resp.json()
                        if stat_data.get("code") == 0:
                            stat = stat_data.get("data", {})
                            if stat:
                                break
                except:
                    continue
            
            # 3. Gabungkan data Quote + Fundamental
            result = {
                "ticker": ticker,
                "name": quote.get("n", ticker),
                "price": quote.get("ld", quote.get("price", 0)),
                "change": quote.get("chp", quote.get("changePercent", 0)),
                "volume": quote.get("v", quote.get("volume", 0)),
                
                # Data Fundamental (sesuaikan key dengan response iTick)
                "market_cap": stat.get("marketCap", stat.get("market_cap", 0)),
                "pe_ratio": stat.get("per", stat.get("pe", 0)),
                "pb_ratio": stat.get("pbv", stat.get("pb", 0)),
                "roe": stat.get("roe", 0),
                "der": stat.get("der", stat.get("debtToEquity", 0)),
                "dividend_yield": stat.get("dividendYield", stat.get("dy", 0)),
                "payout_ratio": stat.get("payoutRatio", stat.get("pr", 0)),
                "revenue_growth_5y": stat.get("revenueGrowth5y", stat.get("revenueGrowth", 0)),
                "profit_growth_5y": stat.get("profitGrowth5y", stat.get("profitGrowth", 0)),
                "sector": stat.get("sector", stat.get("industry", "Unknown")),
                "avg_volume": stat.get("avgVolume", stat.get("avgVol", quote.get("v", 0))),
                "free_float": stat.get("freeFloat", stat.get("free_float", 0)),
            }
            
            # Jika fundamental masih kosong, coba ambil dari Yahoo sebagai fallback
            if result.get("pe_ratio", 0) == 0 and self.use_yfinance:
                print(f"iTick fundamental kosong untuk {ticker}, fallback ke Yahoo")
                yf_data = self._fetch_from_yfinance(ticker)
                if yf_data:
                    # Gabungkan dengan data harga dari iTick
                    yf_data["price"] = result["price"]
                    yf_data["change"] = result["change"]
                    yf_data["volume"] = result["volume"]
                    return yf_data
            
            return result
            
        except Exception as e:
            print(f"iTick error {ticker}: {e}")
            return None
    
    def _fetch_from_yfinance(self, ticker):
        """Ambil data dari Yahoo Finance (ticker diakhiri .JK)"""
        try:
            stock = yf.Ticker(f"{ticker}.JK", session=self.session)
            info = stock.info
            
            # Log untuk debug
            print(f"YFinance {ticker}: PER={info.get('trailingPE', 0)}, ROE={info.get('returnOnEquity', 0)}")
            
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
                "revenue_growth_5y": 0,  # Belum diambil
                "profit_growth_5y": 0,
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
    
    def get_sector_avg_pe(self, sector):
        """Dapatkan rata-rata PER sektor"""
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
