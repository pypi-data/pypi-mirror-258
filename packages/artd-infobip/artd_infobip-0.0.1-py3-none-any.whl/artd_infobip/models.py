from django.db import models
from django.utils.translation import gettext_lazy as _
from artd_partner.models import Partner

class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True

class InfobipCredential(Base):
    """Model definition for Infobip Credential."""
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        verbose_name=_("Partner"),
        help_text=_("Select the partner for which you are creating the Infobip Credential")
    )
    endpoint_url = models.CharField(
        _("Endpoint URL"),
        help_text=_("Infobip endpoint URL"),
        max_length=255
    )
    api_key = models.CharField(
        _("API Key"),
        help_text=_("Infobip API Key"),
        max_length=255
    )

    class Meta:
        """Meta definition for Infobip Credential."""

        verbose_name = 'Infobip Credential'
        verbose_name_plural = 'Infobip Credentials'

    def __str__(self):
        """Unicode representation of Infobip Credential."""
        return f"{self.partner}"

class InfobipSMS(Base):
    """Model definition for Infobip SMS."""
    message_id = models.CharField(
        _("Message ID"),
        help_text=_("Infobip message ID"),
        max_length=255,
        blank=True,
        null=True
    )
    infobip_credential = models.ForeignKey(
        InfobipCredential,
        on_delete=models.CASCADE,
        verbose_name=_("Infobip Credential"),
        help_text=_("Select the Infobip Credential for which you are sending the SMS")
    )
    to = models.CharField(
        _("To"),
        help_text=_("Recipient's phone number"),
        max_length=20
    )
    message = models.TextField(
        _("Message"),
        help_text=_("Message to be sent"),
    )
    response = models.JSONField(
        _("Response"),
        help_text=_("Infobip response"),
        blank=True,
        null=True
    )

    class Meta:
        """Meta definition for Infobip SMS."""

        verbose_name = 'Infobip SMS'
        verbose_name_plural = 'Infobip SMSs'

    def __str__(self):
        """Unicode representation of Infobip SMS."""
        return str(self.id)


