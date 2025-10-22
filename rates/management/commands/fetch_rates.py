import os
import requests
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from rates.models import Rate


API_URL = os.getenv(
    "PB_API_URL",
    "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
)
TARGETS = {"USD", "EUR", "GBP", "PLN"}


class Command(BaseCommand):
    help = "Fetch PrivatBank exchange rates and store a snapshot into rates_db"

    def handle(self, *args, **options):
        try:
            resp = requests.get(API_URL, timeout=15)
            resp.raise_for_status()
            rows = resp.json()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to fetch data: {e}"))
            return

        now = timezone.now()
        created = 0

        for row in rows:
            if row.get("ccy") not in TARGETS:
                continue

            Rate.objects.create(
                ccy=row["ccy"],
                base_ccy=row.get("base_ccy", "UAH"),
                buy=Decimal(str(row["buy"])),
                sale=Decimal(str(row["sale"])),
                source="cards",
                fetched_at=now,
            )
            created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Stored snapshot at {now.strftime('%Y-%m-%d %H:%M:%S')} with {created} rows"
            )
        )
