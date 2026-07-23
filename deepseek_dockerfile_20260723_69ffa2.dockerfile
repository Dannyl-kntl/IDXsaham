# Gunakan image Python 3.12 resmi
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Salin file requirements
COPY requirements.txt .

# Install dependencies (tanpa cache untuk menghemat ukuran)
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file kode
COPY . .

# Jalankan bot
CMD ["python", "bot.py"]