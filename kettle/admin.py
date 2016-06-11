from django.contrib import admin
from .models import Drinker

# Register your models here.

class DrinkerAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name']
    list_display = ('first_name', 'last_name')


admin.site.register(Drinker, DrinkerAdmin)
