FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Запуск через gunicorn (порт 8000 внутри контейнера)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
