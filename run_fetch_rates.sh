#!/usr/bin/env bash
set -euo pipefail

# === Настройки путей ===
PROJECT_DIR="/home/bors/djangoprojects/pb_rates"
VENV_PY="$PROJECT_DIR/venv/bin/python"
LOG_FILE="$PROJECT_DIR/logs/fetch_rates.log"

# === Переходим в каталог проекта ===
cd "$PROJECT_DIR"

# === (опционально) Переменные окружения для БД или API ===
# export RATES_DB_NAME="rates_db"
# export RATES_DB_USER="rates_user"
# export RATES_DB_PASSWORD="rates_password"
# export RATES_DB_HOST="127.0.0.1"

# === Выводим время запуска по Киевскому времени ===
echo "===== $(TZ='Europe/Kiev' date '+%Y-%m-%d %H:%M:%S') (Kyiv time) =====" >> "$LOG_FILE"

# === Запускаем команду Django ===
"$VENV_PY" manage.py fetch_rates >> "$LOG_FILE" 2>&1
