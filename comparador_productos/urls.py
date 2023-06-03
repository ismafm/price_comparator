"""comparador_productos URL Configuration

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
from comparador_productos.views.user_view import login, logout, login_verification, profile, change_info, apply_changes,session_close
from comparador_productos.views.product_view import shw_product, principal_page, search_page, calc_product, save_product
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', principal_page),
    path('search/', search_page),
    path('login/', login),
    path('logout/', logout),
    path('verifylog/', login_verification),
    path('profile/', profile),
    path('calc/', calc_product),
    path('result/', shw_product),
    path('profile/', profile),
    path('info/', change_info),
    path('change/', apply_changes),
    path('close/', session_close),
    path('save/', save_product),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
