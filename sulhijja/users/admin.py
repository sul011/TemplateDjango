from django.contrib import admin
from .models import API, Datadiri

class DatadiriAdmin(admin.ModelAdmin):
    list_display = ('user', 'alamat','telp')
admin.site.register(Datadiri, DatadiriAdmin)

class APIAdmin(admin.ModelAdmin):
    list_display = ('user', 'api_key')
admin.site.register(API, APIAdmin)