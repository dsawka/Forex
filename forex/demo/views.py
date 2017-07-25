from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.template.response import TemplateResponse
from django.views import View
import urllib3, time
from demo.models import DataModel, DealModel
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

class MainView(View):

    def get(self, request):

        transactions_open = DealModel.objects.filter(open_or_closed='OPEN')
        transactions_closed = DealModel.objects.filter(open_or_closed='CLOSED')
        content_dict = {'transactions_open': transactions_open,
                        'transactions_closed': transactions_closed}
        return TemplateResponse(request, 'base.html', content_dict)

    def post(self,request):

        if request.method == 'POST':
            transactions_open = DealModel.objects.filter(open_or_closed='OPEN')
            transactions_closed = DealModel.objects.filter(open_or_closed='CLOSED')
            deal = DataModel.objects.all().last()
            # deal_time = deal.timestamp
            # open_sell_price = deal.ask
            # open_buy_price = deal.bid
            transaction = DealModel.objects.get()
            content_dict = {'answear': '',
                            'transactions_open': transactions_open,
                            'transactions_closed': transactions_closed
                            }
            # deals_id = [transaction.id for transaction in transactions_open]
            # for transaction in transactions_open:
            #     print(transaction.id)


            if request.POST.get('BUY') == 'buy':
                new_deal = {
                    'sell_or_buy': 'buy',
                    'currency': deal.currency,
                    'timestamp': deal.timestamp,
                    'ask': deal.ask,
                    'bid': deal.bid,
                    'low': deal.low,
                    'high': deal.high,
                    'open': deal.open
                    }
                DealModel.objects.create(**new_deal)
                content_dict['answear'] = "Buy %s by %s!" %(deal.currency, deal.bid)

                return render(request, 'base.html', content_dict)

            elif request.POST.get('SELL') == 'sell':
                new_deal = {
                    'sell_or_buy': 'sell',
                    'currency': deal.currency,
                    'timestamp': deal.timestamp,
                    'ask': deal.ask,
                    'bid': deal.bid,
                    'low': deal.low,
                    'high': deal.high,
                    'open': deal.open
                    }
                DealModel.objects.create(**new_deal)
                content_dict['answear'] = "Sell %s by %s!" %(deal.currency, deal.ask)
                return TemplateResponse(request, 'base.html', content_dict)

            elif request.POST.get('name') == transaction.id:
                content_dict['answear'] = "Closed!!!"
                return TemplateResponse(request, 'base.html', content_dict)


            else:
                content_dict['answear'] = "Error!"
                return TemplateResponse(request, 'base.html', content_dict)

# class CloseDealView(View):
#
#     def get(self, request):
#
#         transactions_open = DealModel.objects.filter(open_or_closed='OPEN')
#         transactions_closed = DealModel.objects.filter(open_or_closed='CLOSED')
#         content_dict = {'transactions_open': transactions_open,
#                         'transactions_closed': transactions_closed}
#         return TemplateResponse(request, 'base.html', content_dict)
#
#     def post(self, request, id):
#
#         if request.method == 'POST':
#             transactions_open = DealModel.objects.filter(open_or_closed='OPEN')
#             transactions_closed = DealModel.objects.filter(open_or_closed='CLOSED')
#             DealModel.objects.get(id=id)
#             content_dict = {'answear': '',
#                             'transactions_open': transactions_open,
#                             'transactions_closed': transactions_closed
#                             }
#             transaction_id = request.POST.get('transaction.id')
#             print(transaction_id)
#
#             if request.POST.get('transaction_id') == 'close':
#                 content_dict['answear'] = "Closed!!!"
#                 return TemplateResponse(request, 'base.html', content_dict)













