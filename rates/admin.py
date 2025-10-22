from django.contrib import admin

from .models import Rate


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ("fetched_at", "ccy", "buy", "sale", "source")
    list_filter = ("ccy", "source", "fetched_at")
    ordering = ("-fetched_at",)
