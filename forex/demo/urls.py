from django.conf.urls import url
from django.contrib.auth.views import login, logout, logout_then_login, password_reset, password_reset_confirm, \
    password_reset_done, password_reset_complete, password_change, password_change_done
from . import views

urlpatterns = [

    # Wzorce adresów URL dla widoków logowania i wylogowania.
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),
    url(r'^$', views.dashboard, name='dashboard'),

    # Adresy URL przeznaczone do obsługi zmiany hasła.
    url(r'^password-change/$', password_change, name='password_change'),
    url(r'^password-change/done/$', password_change_done, name='password_change_done'),

    # # Adresy URL przeznaczone do obsługi procedury zerowania hasła.
    url(r'^password-reset/$', password_reset, name='password_reset'),
    url(r'^password-reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', password_reset_complete, name='password_reset_complete'),

    # # Rejestracja konta użytkownika i jego profil.
    url(r'^register/$', views.register, name='register'),
    url(r'^edit/$', views.edit, name='edit'),
]
