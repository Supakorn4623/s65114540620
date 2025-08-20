FROM python:3.10

# ป้องกันการสร้าง .pyc และเปิด log stdout แบบไม่ buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

# ✅ ติดตั้ง dependencies ของ PostgreSQL + netcat
RUN apt-get update \
    && apt-get install -y netcat-openbsd libpq-dev gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# ติดตั้ง dependencies ของ Python
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอก source code ทั้งหมดเข้า container
COPY . /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]