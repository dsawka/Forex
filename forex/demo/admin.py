from django.contrib import admin
from .models import DataModel, DealModel, Profile, Account


# Register your models here.


@admin.register(DataModel)
class DataModelAdmin(admin.ModelAdmin):
    list_display = ('currency', 'date_add', 'timestamp', 'bid', 'ask', 'low', 'high', 'open')


@admin.register(DealModel)
class DealModelAdmin(admin.ModelAdmin):
    list_display = ('currency', 'date_add', 'open_or_closed', 'sell_or_buy', 'timestamp',
                    'bid', 'ask','date_close', 'result', 'user')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'currency', 'equity']
