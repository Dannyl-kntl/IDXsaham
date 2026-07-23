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
        """Jalankan screening untuk semua saham dengan jeda untuk menghindari rate limit"""
        print(f"🔄 Screening {len(IDX_TICKERS)} saham IDX...")
        
        for i, ticker in enumerate(IDX_TICKERS):
            # Tampilkan progress setiap 10 saham
            if i % 10 == 0:
                print(f"  Progress: {i}/{len(IDX_TICKERS)}")
            
            try:
                data = self.fetcher.get_stock_info(ticker)
                if not data:
                    # Jika data kosong, tetap beri jeda lalu lanjut
                    time.sleep(0.6)
                    continue
                
                # Terapkan 10 kriteria screening
                score = self._calculate_score(data)
                if score > 0:
                    data["score"] = score
                    self.results.append(data)
                
                # Jeda 0.6 detik antar permintaan (hindari rate limit)
                time.sleep(0.6)
                
            except Exception as e:
                # Jika terjadi error (misal 429), tunggu lebih lama lalu lanjut
                print(f"⚠️ Error pada {ticker}: {e}")
                print("  Menunggu 5 detik sebelum melanjutkan...")
                time.sleep(5)
                continue
        
        # Urutkan berdasarkan skor tertinggi
        self.results.sort(key=lambda x: x.get("score", 0), reverse=True)
        return self.results[:TOP_N]
    
    def _calculate_score(self, data):
        """Hitung skor berdasarkan 10 kriteria (tidak berubah)"""
        score = 0
        max_score = 100
        
        # 1. PER vs Sektor (makin rendah makin baik)
        pe = data.get("pe_ratio", 0)
        sector_avg = self.fetcher.get_sector_avg_pe(data.get("sector", "Others"))
        if pe > 0 and sector_avg > 0:
            pe_ratio = sector_avg / pe
            pe_score = min(pe_ratio * 5, 20)  # max 20 poin
            score += pe_score
        
        # 2. ROE (makin tinggi makin baik)
        roe = data.get("roe", 0)
        if roe >= MIN_ROE:
            roe_score = min((roe / 20) * 10, 15)  # max 15 poin
            score += roe_score
        
        # 3. DER (makin rendah makin baik)
        der = data.get("der", 0)
        if der <= MAX_DER and der > 0:
            der_score = max(0, (1 - der/MAX_DER) * 10)  # max 10 poin
            score += der_score
        
        # 4. Dividend Yield
        div_yield = data.get("dividend_yield", 0)
        if div_yield >= MIN_DIV_YIELD:
            div_score = min((div_yield / 5) * 10, 10)  # max 10 poin
            score += div_score
        
        # 5. Revenue Growth (5 tahun)
        rev_growth = data.get("revenue_growth_5y", 0)
        if rev_growth > 0:
            growth_score = min(rev_growth / 2, 10)  # max 10 poin
            score += growth_score
        
        # 6. Profit Growth (5 tahun)
        profit_growth = data.get("profit_growth_5y", 0)
        if profit_growth > 0:
            growth_score = min(profit_growth / 2, 10)
            score += growth_score
        
        # 7. Likuiditas (volume)
        avg_vol = data.get("avg_volume", 0)
        if avg_vol > 1000000:
            liq_score = 10
        elif avg_vol > 500000:
            liq_score = 7
        elif avg_vol > 100000:
            liq_score = 4
        else:
            liq_score = 1
        score += liq_score
        
        # 8. Free Float (likuiditas tambahan)
        free_float = data.get("free_float", 0)
        if free_float > 40:
            ff_score = 10
        elif free_float > 20:
            ff_score = 6
        else:
            ff_score = 2
        score += ff_score
        
        # 9. PBV (makin rendah makin baik)
        pbv = data.get("pb_ratio", 0)
        if pbv > 0 and pbv < 1:
            pbv_score = 5
        elif pbv < 2:
            pbv_score = 3
        else:
            pbv_score = 1
        score += pbv_score
        
        # 10. Market Cap (besar = lebih stabil)
        mcap = data.get("market_cap", 0)
        if mcap > 100000000000000:  # >100T
            mcap_score = 5
        elif mcap > 10000000000000:  # >10T
            mcap_score = 3
        else:
            mcap_score = 1
        score += mcap_score
        
        return min(score, max_score)
    
    def format_results(self, results):
        """Format hasil screening untuk Telegram (tidak berubah)"""
        if not results:
            return "⚠️ *Tidak ada saham yang lolos screening hari ini.*"
        
        msg = "📊 *HASIL SCREENING SAHAM IDX* 📊\n"
        msg += f"📅 {pd.Timestamp.now().strftime('%d %B %Y')}\n"
        msg += f"🔍 {len(results)} saham teratas dari {len(IDX_TICKERS)} saham\n"
        msg += "━" * 30 + "\n\n"
        
        for i, stock in enumerate(results, 1):
            msg += f"*{i}. {stock.get('ticker')} — {stock.get('name', '')[:20]}*\n"
            msg += f"  💰 Harga: Rp{stock.get('price', 0):,.0f}\n"
            msg += f"  📊 PER: {stock.get('pe_ratio', 0):.2f}x (Sektor: {self.fetcher.get_sector_avg_pe(stock.get('sector', 'Others')):.2f}x)\n"
            msg += f"  📈 ROE: {stock.get('roe', 0):.1f}% | DER: {stock.get('der', 0):.2f}\n"
            msg += f"  💵 Div.Yield: {stock.get('dividend_yield', 0):.1f}%\n"
            msg += f"  🏷️  Sektor: {stock.get('sector', 'N/A')}\n"
            msg += f"  ⭐ Skor: {stock.get('score', 0):.0f}/100\n"
            msg += "\n"
        
        msg += "━" * 30 + "\n"
        msg += "📌 *Cara baca:* Semakin tinggi skor, semakin baik\n"
        msg += "⚠️ *Disclaimer:* Ini bukan rekomendasi beli/jual.\n"
        msg += "🔍 Ketik /detail [KODE] untuk analisis lengkap"
        
        return msg
    
    def get_detail(self, ticker):
        """Dapatkan detail lengkap 1 saham (tidak berubah)"""
        data = self.fetcher.get_stock_info(ticker)
        if not data:
            return f"❌ Saham {ticker} tidak ditemukan."
        
        sector_avg = self.fetcher.get_sector_avg_pe(data.get("sector", "Others"))
        pe = data.get("pe_ratio", 0)
        pe_discount = ((sector_avg - pe) / sector_avg * 100) if sector_avg > 0 and pe > 0 else 0
        
        # Rating Moat
        moat = self._calculate_moat(data)
        
        # Rating Risiko
        risk_score, risk_reasons = self._calculate_risk(data)
        
        # Target Harga (simplified)
        target_bullish = data.get("price", 0) * 1.3
        target_bearish = data.get("price", 0) * 0.85
        
        # Entry & Stop Loss
        entry_zone = f"Rp{data.get('price', 0) * 0.95:,.0f} - Rp{data.get('price', 0) * 1.05:,.0f}"
        stop_loss = data.get("price", 0) * 0.9
        
        msg = f"""
📊 *DETAIL ANALISIS: {ticker}*
{'━' * 40}

🏢 *Nama:* {data.get('name', 'N/A')}
🏷️ *Sektor:* {data.get('sector', 'N/A')}
💰 *Harga:* Rp{data.get('price', 0):,.0f}

📈 *VALUASI*
• PER: {pe:.2f}x (Sektor: {sector_avg:.2f}x) → {pe_discount:+.1f}% vs sektor
• PBV: {data.get('pb_ratio', 0):.2f}x
• Market Cap: Rp{data.get('market_cap', 0)/1e12:,.1f}T

💪 *FUNDAMENTAL*
• ROE: {data.get('roe', 0):.1f}%
• DER: {data.get('der', 0):.2f}
• Div.Yield: {data.get('dividend_yield', 0):.1f}%
• Payout Ratio: {data.get('payout_ratio', 0):.1f}%

📊 *PERTUMBUHAN 5 TAHUN*
• Revenue Growth: {data.get('revenue_growth_5y', 0):.1f}%
• Profit Growth: {data.get('profit_growth_5y', 0):.1f}%

🛡️ *COMPETITIVE MOAT:* {moat}

⚠️ *RATING RISIKO:* {risk_score}/10
{chr(10).join(['  • ' + r for r in risk_reasons])}

🎯 *TARGET HARGA 12 BULAN*
• Bullish: Rp{target_bullish:,.0f} (+{((target_bullish/data.get('price',1))-1)*100:.0f}%)
• Bearish: Rp{target_bearish:,.0f} ({((target_bearish/data.get('price',1))-1)*100:.0f}%)

📌 *ZONA ENTRY:* {entry_zone}
🛑 *Stop-Loss:* Rp{stop_loss:,.0f}

{'━' * 40}
⚠️ *DISCLAIMER:* Ini adalah alat bantu analisis, bukan rekomendasi investasi. Selalu lakukan riset mandiri.
"""
        return msg
    
    def _calculate_moat(self, data):
        """Hitung rating competitive moat (tidak berubah)"""
        score = 0
        if data.get("market_cap", 0) > 100e12:
            score += 3
        elif data.get("market_cap", 0) > 20e12:
            score += 2
        else:
            score += 1
        
        if data.get("roe", 0) > 20:
            score += 2
        elif data.get("roe", 0) > 15:
            score += 1
        
        moat_sectors = ["Energy", "Infrastructure", "Financial"]
        if data.get("sector") in moat_sectors:
            score += 1
        
        if score >= 5:
            return "🔵 KUAT"
        elif score >= 3:
            return "🟡 SEDANG"
        else:
            return "🟢 LEMAH"
    
    def _calculate_risk(self, data):
        """Hitung rating risiko 1-10 dengan alasan (tidak berubah)"""
        reasons = []
        risk = 0
        
        avg_vol = data.get("avg_volume", 0)
        if avg_vol < 100000:
            risk += 3
            reasons.append("Likuiditas rendah (volume < 100rb)")
        elif avg_vol < 500000:
            risk += 2
            reasons.append("Likuiditas sedang")
        else:
            reasons.append("Likuiditas baik")
        
        ff = data.get("free_float", 0)
        if ff < 20:
            risk += 2
            reasons.append(f"Free float terbatas ({ff:.0f}%)")
        
        der = data.get("der", 0)
        if der > 1.5:
            risk += 2
            reasons.append(f"DER tinggi ({der:.2f})")
        
        change = abs(data.get("change", 0))
        if change > 5:
            risk += 1
            reasons.append("Volatilitas tinggi")
        
        high_risk_sectors = ["Basic Materials", "Energy"]
        if data.get("sector") in high_risk_sectors:
            risk += 1
            reasons.append("Sektor siklikal")
        
        risk = min(risk, 10)
        if not reasons:
            reasons.append("Risiko terkendali")
        
        return risk, reasons[:4]
