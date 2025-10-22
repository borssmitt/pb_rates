import os
import requests
from django.shortcuts import render
from .models import Rate

# URL API Приватбанка (можно переопределить через переменные окружения)
API_URL = os.getenv(
    "PB_API_URL",
    "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
)

# Валюты, которые будем отображать
TARGETS = {"USD", "EUR", "GBP", "PLN"}


def index(request):
    # --- 1. Получаем актуальные курсы валют (онлайн запрос)
    try:
        r = requests.get(API_URL, timeout=10)
        r.raise_for_status()
        data = r.json()  # пример: [{'ccy': 'USD', 'base_ccy': 'UAH', 'buy': '39.50', 'sale': '40.00'}, ...]
        live = [row for row in data if row.get("ccy") in TARGETS]
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        live = []

    # --- 2. Находим последнее сохранённое состояние из базы данных
    latest = Rate.objects.order_by("-fetched_at").first()
    last_ts = latest.fetched_at if latest else None

    if last_ts:
        saved_rows = list(Rate.objects.filter(fetched_at=last_ts))
    else:
        saved_rows = []

    # --- 3. Отображаем страницу с актуальными и сохранёнными курсами
    return render(request, "rates/index.html", {
        "live": live,          # актуальные курсы с API
        "saved": saved_rows,   # последние сохранённые курсы из БД
        "last_ts": last_ts,    # время последнего сохранения
    })
