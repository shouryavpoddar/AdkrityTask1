from django.conf import settings
from django.contrib import admin

from .models import Telecaller, LeadSourceConfig, SalesLead


@admin.action(description='Increase max leads by 1')
def increase_max_leads_by_one(modeladmin, request, queryset):
    for telecaller in queryset:
        telecaller.max_leads += 1
        telecaller.save()


@admin.action(description='Increase max leads by a custom value')
def increase_max_leads_by_custom_value(modeladmin, request, queryset):
    """
    This action increases max_leads by a custom value (set to 5 in this example).
    You can modify the increment value or enhance it to prompt user input.
    """
    increment_value = settings.TELECALLER_INCREMENT_CUSTOM_VALUE  # Change this value if needed
    for telecaller in queryset:
        telecaller.max_leads += increment_value
        telecaller.save()


class TelecallerAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'max_leads',"created", "modified"]  # Adjust fields as per your model
    actions = [increase_max_leads_by_one, increase_max_leads_by_custom_value]

class SalesLeadAdmin(admin.ModelAdmin):
    list_display = ['user', 'telecaller', 'telecaller_role', 'source', 'created', 'modified']  # Adjust fields as per
    list_filter = ['telecaller__role']

class LeadSourceConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'telecallers_list', "filter_logic",'created', 'modified']  # Adjust fields as per your model


admin.site.register(Telecaller, TelecallerAdmin)
admin.site.register(LeadSourceConfig, LeadSourceConfigAdmin)
admin.site.register(SalesLead, SalesLeadAdmin)



# Register your models here.
