from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.template.response import TemplateResponse
from django.views import View
import urllib3, time
from demo.models import DataModel, DealModel, Profile
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib import messages


class MyAccountView(View):
    def get(self, request):

        transactions_open = DealModel.objects.filter(open_or_closed='OPEN')
        transactions_closed = DealModel.objects.filter(open_or_closed='CLOSED')
        content_dict = {'transactions_open': transactions_open,
                        'transactions_closed': transactions_closed}
        return TemplateResponse(request, 'my-account.html', content_dict)

    def post(self, request):

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
            content_dict['answear'] = "Buy %s by %s!" % (deal.currency, deal.bid)

            return render(request, 'my-account.html', content_dict)

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
            content_dict['answear'] = "Sell %s by %s!" % (deal.currency, deal.ask)
            return TemplateResponse(request, 'my-account.html', content_dict)

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
            return TemplateResponse(request, 'my-account.html', content_dict)

        else:
            content_dict['answear'] = "Error!"
            print(vars(request))
            return TemplateResponse(request, 'my-account.html', content_dict)


class TestView(View):
    def get(self, request):
        return TemplateResponse(request, 'test.html')


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Utworzenie nowego obiektu użytkownika, ale jeszcze nie zapisujemy go w bazie danych.
            new_user = user_form.save(commit=False)
            # Ustawienie wybranego hasła.
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Zapisanie obiektu User.
            new_user.save()
            # Utworzenie profilu użytkownika.
            profile = Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Uaktualnienie profilu zakończyło się sukcesem.')
        else:
            messages.error(request, 'Wystąpił błąd podczas uaktualniania profilu.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


class IndexView(View):
    def get(self, request):
        return TemplateResponse(request, 'index.html')

    def post(self, request):

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
            content_dict['answear'] = "Buy %s by %s!" % (deal.currency, deal.bid)

            return render(request, 'my-account.html', content_dict)

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
            content_dict['answear'] = "Sell %s by %s!" % (deal.currency, deal.ask)
            return TemplateResponse(request, 'my-account.html', content_dict)

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
            return TemplateResponse(request, 'my-account.html', content_dict)

        else:
            content_dict['answear'] = "Error!"
            print(vars(request))
            return TemplateResponse(request, 'my-account.html', content_dict)



class ChartsView(View):
    def get(self, request):
        return TemplateResponse(request, 'charts.html')

    def post(self, request):

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
            content_dict['answear'] = "Buy %s by %s!" % (deal.currency, deal.bid)

            return render(request, 'my-account.html', content_dict)

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
            content_dict['answear'] = "Sell %s by %s!" % (deal.currency, deal.ask)
            return TemplateResponse(request, 'my-account.html', content_dict)

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
            return TemplateResponse(request, 'my-account.html', content_dict)

        else:
            content_dict['answear'] = "Error!"
            print(vars(request))
            return TemplateResponse(request, 'my-account.html', content_dict)


class CalendarView(View):
    def get(self, request):
        return TemplateResponse(request, 'calendar.html')
