import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot
BOT_TOKEN = os.getenv("8995282419:AAGf3G7YLLjhwk636BC9rAIgJ6s_ufU2Bp0")

# Data API (pilih salah satu)
# Opsi 1: iTick (gratis, daftar di https://itick.org)
ITICK_API_KEY = os.getenv("c20a0711f786458cb33c849837b97d8738216f7741e14aef91a8d9cd09968251", "")
ITICK_BASE_URL = "https://api.itick.org"

# Opsi 2: Yahoo Finance (fallback, gratis tanpa API key)
USE_YFINANCE_FALLBACK = True

# Konfigurasi Screening
TOP_N = 10
MIN_ROE = 10  # minimum ROE dalam persen
MAX_DER = 2.0  # maksimum DER
MIN_DIV_YIELD = 3.0  # minimum dividend yield dalam persen
MIN_REVENUE_GROWTH = 5.0  # minimum growth 5 tahun dalam persen

# Daftar saham IDX (958 saham) - contoh 50 pertama, Anda bisa tambahkan semua
# Sumber: https://github.com/kevindoni/idx-mcp-server mencakup 958 saham
IDX_TICKERS = [
    "AALI", "ABDA", "ABMM", "ACES", "ADHI", "ADMF", "ADMG", "ADRO", "AGII", "AGRO",
    "AHAP", "AIMS", "AKRA", "ALDO", "ALMI", "AMAG", "AMAR", "AMFG", "AMIN", "AMRT",
    "ANTS", "ANTM", "APEX", "APIC", "APII", "APLI", "APOL", "APRI", "ARCI", "ARII",
    "ARNA", "ARTA", "ARTI", "ASBI", "ASDM", "ASGR", "ASII", "ASJT", "ASMI", "ASRI",
    "ASSA", "ASTI", "ATAP", "AUKA", "AUTM", "AVIA", "BABP", "BACA", "BAJA", "BALI",
    # ... tambahkan hingga 958 saham dari sumber data
    # Untuk daftar lengkap, lihat: https://github.com/kevindoni/idx-mcp-server
]
