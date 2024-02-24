from django.contrib import admin
from artd_openpay.models import OpenPay , OpenPayCard , OpenpayCharge
from django_json_widget.widgets import JSONEditorWidget
from django.db import models


# Register your models here.
@admin.register(OpenPay)
class OpenPayAdmin(admin.ModelAdmin):
    list_display = (
        "production_client_id",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "production_client_id",
        "status",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

@admin.register(OpenPayCard)
class OpenPayCardAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "card_id",
        "brand",
        "card_type",
    )
    list_filter = (
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "customer__email",
        "customer__phone",
        "card_id",
        "brand",
        "card_type",
    )
    readonly_fields = (
        "customer",
        "card_id",
        "brand",
        "card_type",
        "bank_code",
        "bank_name",
        "expiration_month",
        "expiration_year",
        "holder_name",
        "card_number",
    )
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

@admin.register(OpenpayCharge)
class OpenPayChargedAdmin(admin.ModelAdmin):
    list_display = (
        "amount",
        "charge_id",
        "authorization",
        "status"
    )
    list_filter = (
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "amount",
        "charge_id",
        "authorization",
        "status"
    )
    readonly_fields = (
        "card",
        "amount",
        "charge_id",
        "authorization",
        "status"
    )
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }