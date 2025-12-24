from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # <--- THIS IS THE NEW PART --->
    # This function runs once when the server starts.
    # It turns on the "Detective" (loads signals.py)
    def ready(self):
        import accounts.signals