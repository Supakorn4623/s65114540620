FROM python:3.10

WORKDIR /code

# ป้องกัน .pyc และ buffer stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ติดตั้ง dependencies ของ PostgreSQL + netcat
RUN apt-get update && \
    apt-get install -y libpq-dev gcc python3-dev netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

# เก็บ static files
RUN python manage.py collectstatic --noinput || true

# ใช้ gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
