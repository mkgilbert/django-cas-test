"""djangotest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from main import views
from django_cas_ng import views as cas_views


urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^accounts/login$', cas_views.login, name="login"),
    url(r'^accounts/logout$', cas_views.logout, name="logout"),
    url(r'^accounts/callback$', cas_views.callback, name='cas_ng_proxy_callback'),
    url(r'^admin/', admin.site.urls),
]
