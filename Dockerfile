# 1. Базовый образ Python
FROM python:3.12-slim

# 2. Установим зависимости системы
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# 3. Рабочая директория
WORKDIR /app

# 4. Скопируем зависимости и установим их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Скопируем всё приложение
COPY . .

# 6. Переменные окружения Django
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=pb_rates.settings

# 7. Команда запуска сервера (dev mode)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
