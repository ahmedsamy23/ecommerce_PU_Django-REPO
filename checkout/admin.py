from django.contrib import admin
from .models import Address

# Register your models here.


class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street_address', 'apartment_address', 'country', 'zip', 'address_type', 'default')
    list_filter = ('user', 'address_type', 'default')
    search_fields = ('user', 'street_address', 'apartment_address', 'country', 'zip')
    readonly_fields = ('user', 'street_address', 'apartment_address', 'country', 'zip', 'address_type', 'default')

admin.site.register(Address, AddressAdmin)

