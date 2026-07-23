import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, IDX_TICKERS
from screener import StockScreener

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Inisialisasi screener
screener = StockScreener()

# Cache hasil screening (refresh setiap 30 menit)
cache = {
    "results": None,
    "timestamp": None
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /start"""
    welcome = """
🤖 *Selamat datang di IDX Stock Screener Bot!*

Saya adalah bot screening saham IDX dengan 10 kriteria analisis ala Goldman Sachs.

*Perintah yang tersedia:*

/screen — Tampilkan 10 saham teratas IDX
/detail [KODE] — Analisis lengkap 1 saham (contoh: /detail BBCA)
/search [kata] — Cari saham berdasarkan nama
/help — Bantuan

*Contoh penggunaan:*
/screen
/detail INKP
/search bank

⚠️ *Disclaimer:* Ini adalah alat bantu analisis, bukan rekomendasi investasi.
"""
    await update.message.reply_text(welcome, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /help"""
    help_text = """
📖 *PANDUAN PENGGUNAAN*

/screen — Menampilkan 10 saham teratas IDX dengan skor screening
/detail [KODE] — Analisis lengkap 1 saham (PER, ROE, DER, dll)
/search [kata] — Cari saham berdasarkan nama

*Contoh:*
/detail INKP
/search bank

*10 Kriteria Screening:*
1. PER vs rata-rata sektor
2. ROE (Return on Equity)
3. DER (Debt to Equity Ratio)
4. Dividend Yield
5. Pertumbuhan revenue 5 tahun
6. Pertumbuhan laba 5 tahun
7. Likuiditas (volume perdagangan)
8. Free float
9. PBV (Price to Book Value)
10. Market Cap

⚠️ *Peringatan Risiko:*
• Ini BUKAN rekomendasi jual/beli
• Selalu lakukan riset mandiri
• Konsultasikan dengan profesional bersertifikat
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def screen_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /screen"""
    await update.message.reply_text("🔄 *Sedang melakukan screening...*", parse_mode="Markdown")
    
    try:
        # Jalankan screening
        results = screener.run_screening()
        
        # Format hasil
        msg = screener.format_results(results)
        
        # Keyboard untuk detail
        keyboard = []
        row = []
        for i, stock in enumerate(results[:5], 1):
            row.append(InlineKeyboardButton(stock.get("ticker"), callback_data=f"detail_{stock.get('ticker')}"))
            if i % 3 == 0:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        
        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
        
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=reply_markup)
        
    except Exception as e:
        logger.error(f"Error in screen_command: {e}")
        await update.message.reply_text("❌ *Terjadi kesalahan saat screening. Coba lagi nanti.*", parse_mode="Markdown")

async def detail_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /detail [TICKER]"""
    if not context.args:
        await update.message.reply_text("❌ *Masukkan kode saham.*\nContoh: /detail BBCA", parse_mode="Markdown")
        return
    
    ticker = context.args[0].upper()
    await update.message.reply_text(f"🔍 *Menganalisis {ticker}...*", parse_mode="Markdown")
    
    try:
        detail = screener.get_detail(ticker)
        await update.message.reply_text(detail, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in detail_command: {e}")
        await update.message.reply_text(f"❌ *Gagal mengambil data untuk {ticker}.*", parse_mode="Markdown")

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /search [kata]"""
    if not context.args:
        await update.message.reply_text("❌ *Masukkan kata kunci pencarian.*\nContoh: /search bank", parse_mode="Markdown")
        return
    
    keyword = " ".join(context.args).lower()
    results = []
    
    # Cari di daftar ticker (simplified)
    for ticker in IDX_TICKERS:
        if keyword in ticker.lower():
            results.append(ticker)
        if len(results) >= 20:
            break
    
    if results:
        msg = f"🔍 *Hasil pencarian untuk '{keyword}':*\n\n"
        msg += ", ".join([f"`{r}`" for r in results])
        msg += "\n\n💡 Ketik /detail [KODE] untuk analisis lengkap"
        await update.message.reply_text(msg, parse_mode="Markdown")
    else:
        await update.message.reply_text(f"❌ *Tidak ditemukan saham dengan kata '{keyword}'.*", parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk tombol inline"""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("detail_"):
        ticker = query.data.replace("detail_", "")
        detail = screener.get_detail(ticker)
        await query.edit_message_text(detail, parse_mode="Markdown")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk error"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Main function"""
    if not BOT_TOKEN:
        print("❌ ERROR: TELEGRAM_BOT_TOKEN tidak ditemukan di .env")
        print("   Buat file .env dengan isi: TELEGRAM_BOT_TOKEN=your_token_here")
        return
    
    # Buat application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("screen", screen_command))
    app.add_handler(CommandHandler("detail", detail_command))
    app.add_handler(CommandHandler("search", search_command))
    
    # Register callback handler
    app.add_handler(CallbackQueryHandler(button_callback))
    
    # Register error handler
    app.add_error_handler(error_handler)
    
    print("🚀 Bot berjalan! Kirim /start ke bot Telegram Anda.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()