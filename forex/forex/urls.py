"""forex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required

from demo import views
from django.contrib.auth import views as auth_views
from demo.views import TestView, ChartsView, IndexView, MyAccountView, CalendarView
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^my-account/$', login_required(MyAccountView.as_view()), name='my-account'),
    url(r'^test/', TestView.as_view()),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^charts/$', ChartsView.as_view(), name='charts'),
    url(r'^calendar/$', CalendarView.as_view(), name='calendar'),
    url(r'^account/', include('demo.urls')),
    # Social authentication
    # url('social-auth/', include(social.apps.django_app.urls, namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

