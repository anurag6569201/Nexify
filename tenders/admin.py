from django.contrib import admin
from .models import Tender, TenderField

# Registering the Tender model
class TenderFieldInline(admin.TabularInline):
    model = TenderField
    extra = 1  # Add one empty form for TenderField by default

class TenderAdmin(admin.ModelAdmin):
    list_display = ('tender_name', 'tender_id', 'start_date', 'end_date', 'is_active', 'created_at', 'updated_at')
    search_fields = ('tender_name', 'tender_id', 'issued_by')
    list_filter = ('is_active', 'start_date', 'end_date')
    ordering = ('-created_at',)
    inlines = [TenderFieldInline]

admin.site.register(Tender, TenderAdmin)

# Registering the TenderField model
class TenderFieldAdmin(admin.ModelAdmin):
    list_display = ('tender', 'field_name', 'field_value')
    search_fields = ('field_name', 'field_value')

admin.site.register(TenderField, TenderFieldAdmin)
