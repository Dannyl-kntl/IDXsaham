import asyncio
import logging
from datetime import datetime, time
from zoneinfo import ZoneInfo
import requests
from bs4 import BeautifulSoup
import time as time_module

from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, STOCK_LIST
from prefilter import prefilter_stocks
from screener import run_full_screening
from telegram_sender import TelegramSender

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

WITA = ZoneInfo("Asia/Makassar")

# ------------------- SCRAPER IDX (OPSI B) -------------------
def fetch_live_stocks_from_idx() -> list:
    """
    Scrape daftar saham aktif dari IDX.
    Fallback ke STOCK_LIST jika gagal.
    """
    try:
        url = "https://www.idx.co.id/primary/ListedCompany/GetListedCompanies"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        # IDX menggunakan endpoint JSON/AJAX. Kita coba request sederhana.
        # Jika strukturnya berubah, fallback langsung.
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                stocks = []
                for item in data:
                    code = item.get('KodeEfek')
                    if code and code.endswith('.JK') is False:
                        stocks.append(f"{code}.JK")
                if stocks:
                    logger.info(f"[SCRAPER] Berhasil scrape {len(stocks)} saham dari IDX.")
                    return stocks
        # Jika gagal, coba scrape halaman statis
        url2 = "https://www.idx.co.id/id/beranda/daftar-saham/"
        response = requests.get(url2, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Cari table atau dropdown (struktur sering berubah)
            # Kita akan ambil dari opsi select jika ada
            select = soup.find('select', {'id': 'id_stock'})
            if select:
                stocks = [opt.text.strip().split(' ')[0] + '.JK' for opt in select.find_all('option') if opt.text.strip()]
                if stocks:
                    logger.info(f"[SCRAPER] Alternatif: scrape {len(stocks)} saham.")
                    return stocks
    except Exception as e:
        logger.error(f"[SCRAPER] Gagal scrape: {e}")
        # Kirim notifikasi error ke Telegram
        sender = TelegramSender()
        sender.send_error_log(
            f"Gagal update daftar saham dari IDX.\n"
            f"Error: {str(e)}\n"
            f"Falling back ke static list ({len(STOCK_LIST)} saham).\n"
            f"Mohon perbaiki mekanisme scraping untuk update otomatis."
        )
    # Fallback ke static list
    return STOCK_LIST

async def update_stock_list():
    """Fungsi async untuk update daftar saham (dipanggil mingguan)"""
    logger.info("⏳ Updating stock list from IDX...")
    new_list = fetch_live_stocks_from_idx()
    if new_list and len(new_list) > 100:
        # Update global variable (hati-hati di production, lebih baik simpan ke file/config)
        # Untuk sementara, karena kita pakai config import, kita simpan ke file atau env.
        # Atau kita patch di sini: bot akan pakai list ini untuk screening.
        global ACTIVE_STOCK_LIST
        ACTIVE_STOCK_LIST = new_list
        logger.info(f"✅ Stock list updated to {len(ACTIVE_STOCK_LIST)} stocks.")
    else:
        logger.warning("⚠️ Gagal update, tetap pakai static list.")

# Global list yang akan dipakai (awal dari config)
ACTIVE_STOCK_LIST = STOCK_LIST

# ------------------- SCREENING ENGINE -------------------
async def run_screening_flow(session: str):
    """Alur screening 2 tahap"""
    logger.info(f"Starting screening {session}...")
    sender = TelegramSender()
    
    # Tahap 1: Prefilter (30 hari)
    passed_tickers, infos = prefilter_stocks()
    if not passed_tickers:
        await sender.send_screening([], f"{session} - No stocks passed filter")
        return
    
    # Tahap 2: Full Analysis (6 bulan)
    results = run_full_screening(passed_tickers)
    
    # Kirim hasil
    await sender.send_screening(results, session)

# ------------------- TELEGRAM HANDLERS -------------------
async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("🔍 Screen Now", callback_data="screen")],
        [InlineKeyboardButton("📊 Refresh List (Scrape)", callback_data="refresh")],
        [InlineKeyboardButton("⏰ Schedule Info", callback_data="schedule")],
    ]
    await update.message.reply_text(
        "🤖 *IDX 1000+ Screener Bot*\n\n"
        "Auto-screen daily at *15:30 WITA* (afternoon).\n"
        "Results for next day's trading.\n\n"
        "Features: Zombie filter, Entry/SL/TP (ATR), Patterns, Breakout detection.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def screen_now(update, context):
    await update.message.reply_text("⏳ Screening in progress... (2-stage, ~5-7 mins)")
    await run_screening_flow("Manual")
    await update.message.reply_text("✅ Done.")

async def refresh_stocks(update, context):
    await update.message.reply_text("⏳ Fetching latest stock list from IDX...")
    global ACTIVE_STOCK_LIST
    new_list = fetch_live_stocks_from_idx()
    if new_list and len(new_list) > 100:
        ACTIVE_STOCK_LIST = new_list
        await update.message.reply_text(f"✅ Updated to {len(ACTIVE_STOCK_LIST)} stocks.")
    else:
        await update.message.reply_text("⚠️ Failed to fetch, using static list.")

async def button_handler(update, context):
    query = update.callback_query
    await query.answer()
    if query.data == "screen":
        await query.message.reply_text("⏳ Screening...")
        await run_screening_flow("Manual")
    elif query.data == "refresh":
        global ACTIVE_STOCK_LIST
        new_list = fetch_live_stocks_from_idx()
        if new_list and len(new_list) > 100:
            ACTIVE_STOCK_LIST = new_list
            await query.message.reply_text(f"✅ Updated to {len(ACTIVE_STOCK_LIST)} stocks.")
        else:
            await query.message.reply_text("⚠️ Failed, using static list.")
    elif query.data == "schedule":
        await query.message.reply_text(
            "⏰ *Schedule*\n\n"
            "• Daily: 15:30 WITA (Afternoon scan)\n"
            "  (Market closes at 16:50 WITA, results for next day)\n"
            "• Weekly: Sunday 23:00 WITA (Update stock list from IDX)",
            parse_mode="Markdown"
        )

# ------------------- SCHEDULED JOBS -------------------
async def scheduled_screening(context):
    await run_screening_flow("Afternoon Scan")

async def scheduled_scrape(context):
    global ACTIVE_STOCK_LIST
    logger.info("Running weekly stock list update...")
    new_list = fetch_live_stocks_from_idx()
    if new_list and len(new_list) > 100:
        ACTIVE_STOCK_LIST = new_list
        logger.info(f"Weekly update success: {len(ACTIVE_STOCK_LIST)} stocks.")
    else:
        logger.warning("Weekly update failed, keeping static list.")

# ------------------- MAIN -------------------
def main():
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error("Missing TELEGRAM_TOKEN or CHAT_ID in .env")
        return

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("screen", screen_now))
    app.add_handler(CommandHandler("refresh", refresh_stocks))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # Jobs
    job_queue = app.job_queue
    # Daily 15:30 WITA
    job_queue.run_daily(
        scheduled_screening,
        time=time(hour=15, minute=30, tzinfo=WITA),
        name="daily_screen"
    )
    # Weekly Sunday 23:00 WITA (update list)
    job_queue.run_daily(
        scheduled_scrape,
        time=time(hour=23, minute=0, tzinfo=WITA),
        days=(6,),  # Sunday = 6 (Monday=0)
        name="weekly_scrape"
    )
    
    logger.info("🚀 Bot started. Daily scan at 15:30 WITA. Weekly scrape Sunday 23:00 WITA.")
    app.run_polling()

if __name__ == "__main__":
    main()
