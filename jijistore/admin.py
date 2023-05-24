from django.contrib import admin
from jijistore.models import Items

# Register your models here.
@admin.register(Items)
class storeAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'date_uploaded', 'price']


# @admin.register(Store)
# class storeAdmin(admin.ModelAdmin):
#     list_display = ['name', 'author', 'create_date']
