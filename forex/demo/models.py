from django.db import models
from django.conf import settings


SELL_OR_BUY = (
    ('sell', 'sell'),
    ('buy', 'buy')
)
OPEN_OR_CLOSED = (
    ('Open', 'OPEN'),
    ('Closed', 'CLOSED')
)
CURRENCY = (
    ('EUR', 'EUR'),
    ('USD', 'USD')
)

class DataModel(models.Model):
    date_add = models.DateTimeField(auto_now_add=True, db_index=True)
    timestamp = models.BigIntegerField(db_index=True)
    currency = models.CharField(max_length=16)
    ask = models.FloatField()
    bid = models.FloatField()
    low = models.FloatField()
    high = models.FloatField()
    open = models.FloatField()

    def __str__(self):
        return "%s Ask: %s Bid: %s" % (self.currency, self.ask, self.bid)


class DealModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    sell_or_buy = models.CharField(max_length=16, choices=SELL_OR_BUY, null=True)
    date_add = models.DateTimeField(auto_now_add=True, db_index=True)
    open_or_closed = models.CharField(max_length=16, choices=OPEN_OR_CLOSED, default='Open')
    timestamp = models.BigIntegerField(db_index=True)
    currency = models.CharField(max_length=16)
    ask = models.FloatField()
    bid = models.FloatField()
    low = models.FloatField()
    high = models.FloatField()
    open = models.FloatField()
    result = models.DecimalField(null=True, max_digits=6, decimal_places=5)

    def __str__(self):
        return "%s, %s, %s" % (self.sell_or_buy, self.ask, self.bid)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d',
                              blank=True)

    def __str__(self):
        return 'Profil użytkownika {}.'.format(self.user.username)


class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    currency = models.CharField(max_length=16, choices=CURRENCY, default='USD')
    equity = models.DecimalField(max_digits=9, decimal_places=2, default=10000)

    def __str__(self):
        return "{}'s account" .format(self.user.username)
