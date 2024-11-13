from django.contrib import admin
from .models import Relay, DH11

class RelayAdmin(admin.ModelAdmin):
    list_display = ('name', 'mac_addr', 'state')

class DH11Admin(admin.ModelAdmin):
    list_display = ('name', 'mac_addr', 'temp', 'humidity')

admin.site.register(Relay, RelayAdmin)
admin.site.register(DH11, DH11Admin)
