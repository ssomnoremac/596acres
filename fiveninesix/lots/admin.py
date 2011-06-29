from django.contrib import admin

from models import Lot, Owner, OwnerType

class LotAdmin(admin.ModelAdmin):
    search_fields = ('address', 'bbl')
    list_display = ('address', 'borough', 'bbl', 'zipcode', 'owner', 'area',)
    ordering = ('address',)

class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'phone', 'type',)
    ordering = ('name',)

class OwnerTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

admin.site.register(Lot, LotAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(OwnerType, OwnerTypeAdmin)