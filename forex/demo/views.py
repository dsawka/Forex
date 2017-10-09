from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views import View
from demo.models import DataModel, DealModel, Profile, Account
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib import messages
from django.urls import reverse

class IndexView(View):
    def get(self, request):

        return TemplateResponse(request, 'main/index.html')

    def post(self, request):

        deal = DataModel.objects.all().last()
        if request.user.is_authenticated:

            if request.POST.get('BUY') == 'buy':
                new_deal = {
                    'user': request.user,
                    'sell_or_buy': 'buy',
                    'currency': deal.currency,
                    'timestamp': deal.timestamp,
                    'bid': deal.bid,
                    'ask': deal.ask,
                    'low': deal.low,
                    'high': deal.high,
                    'open': deal.open
                }
                DealModel.objects.create(**new_deal)
                return HttpResponseRedirect(reverse('my-account'))

            elif request.POST.get('SELL') == 'sell':
                new_deal = {
                    'user': request.user,
                    'sell_or_buy': 'sell',
                    'currency': deal.currency,
                    'timestamp': deal.timestamp,
                    'bid': deal.bid,
                    'ask': deal.ask,
                    'low': deal.low,
                    'high': deal.high,
                    'open': deal.open
                }
                DealModel.objects.create(**new_deal)
                return HttpResponseRedirect(reverse('my-account'))
        else:
            return HttpResponseRedirect(reverse('login'))

class ChartsView(View):

    def get(self, request):
        return TemplateResponse(request, 'main/charts.html')

    def post(self, request):

        deal = DataModel.objects.all().last()
        if request.user.is_authenticated:

            if request.POST.get('BUY') == 'buy':
                new_deal = {
                    'user': request.user,
                    'sell_or_buy': 'buy',
                    'currency': deal.currency,
                    'timestamp': deal.timestamp,
                    'bid': deal.bid,
                    'ask': deal.ask,
                    'low': deal.low,
                    'high': deal.high,
                    'open': deal.open
                }
                DealModel.objects.create(**new_deal)
                return HttpResponseRedirect(reverse('my-account'))

            elif request.POST.get('SELL') == 'sell':
                new_deal = {
                    'user': request.user,
                    'sell_or_buy': 'sell',
                    'currency': deal.currency,
                    'timestamp': deal.timestamp,
                    'bid': deal.bid,
                    'ask': deal.ask,
                    'low': deal.low,
                    'high': deal.high,
                    'open': deal.open
                }
                DealModel.objects.create(**new_deal)
                return HttpResponseRedirect(reverse('my-account'))
        else:
            return HttpResponseRedirect(reverse('login'))


class CalendarView(View):
    def get(self, request):
        return TemplateResponse(request, 'main/calendar.html')


class MyAccountView(View):
    def get(self, request):

        transactions_open = DealModel.objects.filter(user=request.user, open_or_closed='OPEN')
        transactions_closed = DealModel.objects.filter(user=request.user, open_or_closed='CLOSED')
        profit_pips = transactions_closed.aggregate(Sum('result'))
        profit_pips = profit_pips.get('result__sum')
        user_account = Account.objects.get(user=request.user)
        if profit_pips is not None:
            user_account.profit = profit_pips * 100000
            user_account.save()
        user_profit = user_account.profit
        content_dict = {'transactions_open': transactions_open,
                        'transactions_closed': transactions_closed,
                        'profit': user_profit
                        }
        return TemplateResponse(request, 'main/my-account.html', content_dict)

    def post(self, request):

        transactions_open = DealModel.objects.filter(user=request.user, open_or_closed='OPEN')
        transactions_closed = DealModel.objects.filter(user=request.user, open_or_closed='CLOSED')
        deal = DataModel.objects.all().last()
        content_dict = {'transactions_open': transactions_open,
                        'transactions_closed': transactions_closed,
                        'profit': ''
                        }
        if 'close' in request.POST.values():
            for key, value in request.POST.items():
                if value == 'close':
                    deal_id = key

        if request.POST.get(deal_id) == 'close':
            closing_deal = DealModel.objects.get(id=deal_id)
            closing_deal.open_or_closed = 'Closed'
            closing_deal.save()
            if closing_deal.sell_or_buy == 'sell':
                result = closing_deal.bid - deal.ask
                closing_deal.result = result
                closing_deal.save()
            if closing_deal.sell_or_buy == 'buy':
                result = deal.bid - closing_deal.ask
                closing_deal.result = result
                closing_deal.save()

            profit_pips = transactions_closed.aggregate(Sum('result'))
            profit_pips = profit_pips.get('result__sum')
            user_account = Account.objects.get(user=request.user)
            if profit_pips is not None:
                user_account.profit = profit_pips * 100000
                user_account.save()
            user_profit = user_account.profit
            content_dict ['profit'] = user_profit
            return TemplateResponse(request, 'main/my-account.html', content_dict)

        else:
            content_dict['answear'] = "Error!"
            print(vars(request))
            return TemplateResponse(request, 'main/my-account.html', content_dict)


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
            Account.objects.create(user=new_user)
            Profile.objects.create(user=new_user)
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






