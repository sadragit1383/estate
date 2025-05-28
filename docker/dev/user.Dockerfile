FROM python:3.9-slim

WORKDIR /app

# نصب پیش‌نیازهای سیستمی
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# کپی فایل‌های پروژه
COPY ./apps/user/ /app/

# نصب نیازمندی‌های پایتون
RUN pip install --no-cache-dir -r requirements.txt

CMD ["watchmedo", "auto-restart", \
     "--directory=./", \
     "--pattern=*.py", \
     "--recursive", \
     "--", "python", "manage.py", "runserver", "0.0.0.0:8001"]