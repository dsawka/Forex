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

        transactions_open = DealModel.objects.filter(open_or_closed='OPEN')
        transactions_closed = DealModel.objects.filter(open_or_closed='CLOSED')
        deal = DataModel.objects.all().last()

        content_dict = {'answear': '',
                        'transactions_open': transactions_open,
                        'transactions_closed': transactions_closed
                        }

        if 'close' in request.POST.values():
            for key, value in request.POST.items():
                if value == 'close':
                    deal_id = key

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

        elif request.POST.get(deal_id) == 'close':
            closing_deal = DealModel.objects.get(id=deal_id)
            closing_deal.open_or_closed = 'Closed'
            closing_deal.save()
            if closing_deal.sell_or_buy == 'sell':
                result = closing_deal.ask - deal.bid
                closing_deal.result = result
                closing_deal.save()
            if closing_deal.sell_or_buy == 'buy':
                result = deal.ask - closing_deal.bid
                closing_deal.result = result
                closing_deal.save()

            content_dict['answear'] = "Closed!!!"
            return TemplateResponse(request, 'base.html', content_dict)

        else:
            content_dict['answear'] = "Error!"
            print(vars(request))
            return TemplateResponse(request, 'base.html', content_dict)














