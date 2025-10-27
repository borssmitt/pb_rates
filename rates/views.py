import os
import requests
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Max
from .models import Rate

API_URL = os.getenv(
    "PB_API_URL",
    "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
)

TARGETS = {"USD", "EUR", "GBP", "PLN"}


def index(request):
    # --- 1. Получаем актуальные курсы валют
    try:
        r = requests.get(API_URL, timeout=10)
        r.raise_for_status()
        data = r.json()
        live = [row for row in data if row.get("ccy") in TARGETS]
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        live = []

    # --- 2. Сохраняем данные в базу
    if live:
        ts = timezone.now()
        for row in live:
            try:
                Rate.objects.create(
                    ccy=row["ccy"],
                    base_ccy=row["base_ccy"],
                    buy=float(row["buy"]),
                    sale=float(row["sale"]),
                    source="cash",
                    fetched_at=ts,
                )
            except Exception as e:
                print(f"Ошибка при сохранении {row}: {e}")

    # --- 3. ВАЖНО: правильный способ выбрать все валюты из последнего снимка ---
    last_ts = Rate.objects.aggregate(last=Max("fetched_at"))["last"]
    saved = Rate.objects.filter(fetched_at__gte=last_ts - timezone.timedelta(seconds=1)).order_by("ccy")

    # --- 4. Отображаем данные ---
    return render(request, "rates/index.html", {
        "live": live,
        "saved": saved,
        "last_ts": last_ts,
    })
