from django.db import models

class Rate(models.Model):
    SOURCE_CHOICES = (
        ("cards", "Non-cash (cards)"),
        ("cash", "Cash"),
    )

    ccy = models.CharField(max_length=3)          # USD, EUR, GBP, PLN
    base_ccy = models.CharField(max_length=3)     # usually UAH
    buy = models.DecimalField(max_digits=10, decimal_places=4)
    sale = models.DecimalField(max_digits=10, decimal_places=4)
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default="cards")
    fetched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "rates"
        ordering = ["-fetched_at", "ccy"]

    def __str__(self):
        return f"{self.ccy}/{self.base_ccy} buy={self.buy} sale={self.sale}"
