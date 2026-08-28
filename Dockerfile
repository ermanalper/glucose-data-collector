FROM python:3.14-slim

# Konteyner içindeki çalışma dizinini belirliyoruz
WORKDIR /app
ENV PYTHONUNBUFFERED=1 
#BUFFER YOK. FORCE PRINT
# Önce sadece requirements.txt dosyasını kopyalıyoruz (Cache optimizasyonu için)
COPY requirements.txt .

# Bağımlılıkları kuruyoruz
RUN pip install --no-cache-dir -r requirements.txt

# Kalan tüm proje dosyalarını kopyalıyoruz
COPY . .

# Python scriptini başlatıyoruz (script adınız main.py ise)
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]