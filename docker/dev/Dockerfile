FROM python:3.9-slim

WORKDIR /app

# نصب پیش‌نیازهای سیستمی
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# نصب پکیج‌ها (شامل watchdog)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# استفاده از watchmedo برای ریلود خودکار
CMD ["watchmedo", "auto-restart", \
     "--directory=./", \
     "--pattern=*.py", \
     "--recursive", \
     "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]