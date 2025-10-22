class RatesRouter:
    """Send the rates.Rate model to the 'rates_db' database only."""


app_label = "rates"
model_name = "rate"


def db_for_read(self, model, **hints):
    if model._meta.app_label == self.app_label:
        return "rates_db"
        return None


def db_for_write(self, model, **hints):
    if model._meta.app_label == self.app_label:
        return "rates_db"
        return None


def allow_migrate(self, db, app_label, model_name=None, **hints):
    if app_label == self.app_label:
        return db == "rates_db"
        return None