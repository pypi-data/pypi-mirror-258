from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _



class ArtdOpenpayConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "artd_openpay"
    verbose_name = _("Artd Open Pay")
