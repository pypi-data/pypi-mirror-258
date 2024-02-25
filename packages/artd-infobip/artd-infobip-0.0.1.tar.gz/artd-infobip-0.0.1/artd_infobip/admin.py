from django.contrib import admin
from artd_infobip.models import InfobipCredential, InfobipSMS
from django_json_widget.widgets import JSONEditorWidget
from django.db import models

@admin.register(InfobipCredential)
class InfobipCredentialAdmin(admin.ModelAdmin):
    list_display = ["partner", "endpoint_url", "api_key", "status",]
    list_filter = ["partner", "status",]
    search_fields = ["partner", "endpoint_url", "api_key",]
    list_per_page = 20
    fieldsets = (
        (
            "Credentials",
            {
                "fields": (
                    "partner",
                    "endpoint_url",
                    "api_key",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "status",
                )
            },
        ),
    )
    readonly_fields = ["created", "updated"]

@admin.register(InfobipSMS)
class InfobipSMSAdmin(admin.ModelAdmin):
    list_display = ["message_id","infobip_credential", "id", "to", "message", "status",]
    list_filter = ["infobip_credential", "status",]
    search_fields = ["infobip_credential", "to", "message",]
    list_per_page = 20
    fieldsets = (
        (
            "SMS",
            {
                "fields": (
                    "message_id",
                    "infobip_credential",
                    "to",
                    "message",
                )
            },
        ),
        (
            "Response",
            {
                "fields": (
                    "response",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "status",
                )
            },
        ),
    )
    readonly_fields = ["message_id", "infobip_credential", "to", "message", "created", "updated"]
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }