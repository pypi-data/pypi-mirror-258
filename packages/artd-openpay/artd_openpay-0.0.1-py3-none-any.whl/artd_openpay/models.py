from django.db import models
from django.utils.translation import gettext_lazy as _
from artd_partner.models import Partner
from artd_customer.models import Customer

class Base(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    status = models.BooleanField(
        "status",
        default=True,
    )

    class Meta:
        abstract = True

class OpenPay(Base):
    """Model definition for MercadoPago."""

    partner = models.ForeignKey(
        Partner,
        help_text=_("Partner"),
        on_delete=models.CASCADE,
        
    )

    production_client_id = models.CharField(
        _("Production client id"),
        help_text=_("Production client id"),
        max_length=250,
    )
    production_client_secret = models.CharField(
        _("Production client secret"), 
        help_text=_("Production client secret"),
        max_length=250,
    )
    production_public_key = models.CharField(
        _("Production public key"),
        help_text=_("Production public key"),
        max_length=250,
    )

    class Meta:
        """Meta definition for OpenPay."""

        verbose_name = "Open Pay"
        verbose_name_plural = "Open Pay"

    def __str__(self):
        return str(self.id)
        """Unicode representation of OpenPay."""

class OpenPayCard(Base):
    customer = models.ForeignKey(
        Customer,
        help_text=_("Customer"),
        on_delete=models.CASCADE,
    )

    bank_code = models.CharField(
        _("Bank Code"),
        help_text=_("Bank Code"),
        max_length=250,
    )
    bank_name = models.CharField(
        _("Bank Name"),
        help_text=_("Bank Name"),
        max_length=250,
    )
    brand = models.CharField(
        _("Brand"),
        help_text=_("Brand"),
        max_length=250,
    )
    card_number = models.CharField(
        _("Card Number"),
        help_text=_("Card Number"),
        max_length=250,
    )
    expiration_month = models.CharField(
        _("Expiration Month"),
        help_text=_("Expiration Month"),
        max_length=250,
    )
    expiration_year = models.CharField(
        _("Expiration Year"),
        help_text=_("Expiration Year"),
        max_length=250,
    )
    holder_name = models.CharField(
        _("Holder Name"),
        help_text=_("Holder Name"),
        max_length=250,
    )
    card_id = models.CharField(
        _("Card Id"),
        help_text=_("Card Id"),
        max_length=250,
    )
    card_type = models.CharField(
        _("Card Type"),
        help_text=_("Card Type"),
        max_length=250,
    )
    other_data = models.JSONField(
        help_text=_("Card Type"),
        null = True,
        blank = True,
        default = dict
    )

    class Meta:
        """Meta definition for OpenPay."""

        verbose_name = "Open Pay Card"
        verbose_name_plural = "Open Pay Cards"

    def __str__(self):
        return str(self.card_id)
        """Unicode representation of OpenPay."""

class OpenpayCharge(Base):

    card = models.ForeignKey(
        OpenPayCard,
        help_text=_("Card Id"),
        on_delete=models.CASCADE,
    )
    amount = models.FloatField(
        _("Charge Amount"),
        help_text=_("Charge Amounts"),
        default = 0
    )
    charge_id = models.CharField(
        _("Charge id"),
        help_text=_("Charge id"),
        max_length=250,
    )
    authorization = models.CharField(
        _("Charge Authorization"),
        help_text=_("Charge Authorizations"),
        max_length=250,
    )
    status = models.CharField(
        _("Charge Status"),
        help_text=_("Charge Status"),
        max_length=250,
    )
    other_data = models.JSONField(
        help_text=_("Card Charge"),
        null = True,
        blank = True,
        default = dict
    )
    class Meta:
        """Meta definition for OpenPay."""

        verbose_name = "Open Pay Charge"
        verbose_name_plural = "Open Pay Charges"

    def __str__(self):
        return str(self.charge_id)
        """Unicode representation of OpenPay."""




