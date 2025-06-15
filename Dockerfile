# ✅ Base image: Python resmi, versi terbaru disarankan
FROM python:3.11-slim

# ✅ Atur direktori kerja di container
WORKDIR /app

# ✅ Salin file ke dalam container
COPY . /app

# ✅ Upgrade pip & install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ✅ Expose port FastAPI
EXPOSE 8000

# ✅ Perintah default untuk run uvicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
