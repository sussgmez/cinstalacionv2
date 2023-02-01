"""cinstalacionv2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from agenda.views import redirect_agenda, agenda, tecnicos_json, instalaciones_json, guardar, create_instalacion, update_instalacion, login_view, logout_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_agenda),
    path('accounts/login/', login_view, name="login"),
    path('accounts/logout/', logout_view, name="logout"),
    path('agenda/', agenda, name="agenda"),
    path('tecnicos/json', tecnicos_json, name='tecnicos_json'),
    path('instalaciones/json', instalaciones_json, name='instalaciones_json'),
    path('instalaciones/guardar', guardar, name='guardar'),
    path('instalaciones/create_instalacion', create_instalacion, name='create_instalacion'),
    path('instalaciones/update_instalacion/<slug:nro_contrato>', update_instalacion, name='update_instalacion'),
]
