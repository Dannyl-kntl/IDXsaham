from telegram import Bot
from telegram.error import TelegramError
import logging
from typing import List, Dict
from datetime import datetime
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)

class TelegramSender:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_TOKEN) if TELEGRAM_TOKEN else None
        self.chat_id = TELEGRAM_CHAT_ID

    def _format_message(self, results: List[Dict], session: str) -> str:
        if not results:
            return "⚠️ No signals found today."

        # Kategorisasi
        strong_buy = [r for r in results if r['score'] >= 5]
        buy = [r for r in results if 3 <= r['score'] < 5]
        breakout = [r for r in results if r.get('is_breakout', False)]
        sell = [r for r in results if r['score'] <= -2]
        # Neutral (1-2) tidak ditampilkan di ringkasan utama

        now = datetime.now()
        lines = [
            f"📊 IDX SCREENING - {session}",
            f"🕐 {now.strftime('%d-%b %H:%M WITA')}",
            f"📈 Total analyzed: {len(results)}",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ]

        # 1. STRONG BUY
        if strong_buy:
            lines.append("🟢 STRONG BUY (Score ≥5)")
            for r in strong_buy[:10]:
                lines.append(
                    f"  • *{r['ticker']}* | Rp{r['price']:,.0f} | Δ{r['change']:+.1f}% | "
                    f"RSI {r['rsi']:.0f} | RR {r['rr_ratio']:.1f}x"
                )
                lines.append(
                    f"    Entry: {r['entry']:,.0f} | SL: {r['stop_loss']:,.0f} | "
                    f"TP1: {r['take_profit_1']:,.0f} | TP2: {r['take_profit_2']:,.0f}"
                )
                if r['signals']:
                    lines.append(f"    🧠 {', '.join(r['signals'][:3])}")
                if r['patterns']:
                    lines.append(f"    🔍 Patterns: {', '.join(r['patterns'])}")
            lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # 2. STRONG BREAKOUT POTENTIAL (kategori khusus)
        if breakout:
            lines.append("🚀 *STRONG BREAKOUT POTENTIAL*")
            for r in breakout[:5]:
                lines.append(
                    f"  • *{r['ticker']}* | Rp{r['price']:,.0f} | Vol {r['volume_ratio']:.1f}x avg | "
                    f"Score {r['score']}"
                )
                lines.append(
                    f"    Entry: {r['entry']:,.0f} | TP1: {r['take_profit_1']:,.0f}"
                )
            lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # 3. BUY
        if buy:
            lines.append("🟡 BUY (Score 3-4)")
            for r in buy[:5]:
                lines.append(
                    f"  • *{r['ticker']}* | Rp{r['price']:,.0f} | Δ{r['change']:+.1f}% | "
                    f"RSI {r['rsi']:.0f} | Score {r['score']}"
                )
            lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # 4. SELL (warning)
        if sell:
            lines.append("🔴 SELL / OVERBOUGHT")
            for r in sell[:5]:
                lines.append(
                    f"  • *{r['ticker']}* | Rp{r['price']:,.0f} | RSI {r['rsi']:.0f} | "
                    f"Score {r['score']}"
                )
            lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # 5. TOP 10 OVERALL (Score Tertinggi + pola)
        lines.append("🏆 *TOP 10 SCORE OVERALL*")
        for i, r in enumerate(results[:10], 1):
            emoji = "🟢" if r['score'] >= 5 else "🟡" if r['score'] >= 3 else "⚪"
            lines.append(
                f"{i}. {emoji} *{r['ticker']}* | Rp{r['price']:,.0f} | Δ{r['change']:+.1f}% | "
                f"Score {r['score']} | RR {r['rr_ratio']:.1f}x"
            )
            if r['patterns']:
                lines.append(f"   🔍 {', '.join(r['patterns'][:2])}")

        lines.append("")
        lines.append("---")
        lines.append("💡 *Guide:* Score ≥5 SB, 3-4 Buy, -2 to 2 Neutral, ≤ -2 Sell")
        lines.append("📌 SL = Entry - (ATR×1.5) | TP1 = Entry + (ATR×2) | TP2 = Entry + (ATR×3.5)")
        lines.append("⚠️ Edu only, not financial advice.")

        return "\n".join(lines)

    def send_screening(self, results: List[Dict], session: str) -> bool:
        if not self.bot:
            logger.error("Telegram bot not ready.")
            return False

        msg = self._format_message(results, session)
        try:
            if len(msg) > 4000:
                # Split jadi beberapa pesan
                parts = [msg[i:i+4000] for i in range(0, len(msg), 4000)]
                for idx, part in enumerate(parts):
                    prefix = f"📄 Part {idx+1}/{len(parts)}\n\n" if len(parts) > 1 else ""
                    self.bot.send_message(self.chat_id, prefix + part, parse_mode="Markdown")
            else:
                self.bot.send_message(self.chat_id, msg, parse_mode="Markdown")
            logger.info(f"Screening {session} sent.")
            return True
        except TelegramError as e:
            logger.error(f"Send error: {e}")
            return False

    def send_error_log(self, error_msg: str) -> bool:
        """Kirim error penting ke Telegram (misal gagal scrape)"""
        if not self.bot:
            return False
        try:
            self.bot.send_message(
                self.chat_id,
                f"⚠️ *BOT ERROR*\n\n{error_msg}",
                parse_mode="Markdown"
            )
            return True
        except:
            return False