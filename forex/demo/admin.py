from django.contrib import admin
from .models import DataModel, DealModel
# Register your models here.


@admin.register(DataModel)
class DataModelAdmin(admin.ModelAdmin):

    list_display = ('currency', 'date_add', 'timestamp', 'ask', 'bid', 'low','high', 'open')


@admin.register(DealModel)
class DealModelAdmin(admin.ModelAdmin):

    list_display = ('currency', 'date_add', 'open_or_closed', 'sell_or_buy', 'timestamp', 'ask', 'bid', 'low','high', 'open')