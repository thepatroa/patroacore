from django.contrib import admin

from .models import Firm, FirmMember

admin.site.register(Firm)
admin.site.register(FirmMember)
