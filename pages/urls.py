from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('new_account', views.new_account, name='new_account'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('dashboard', views.dashboard, name='dashboard'),
]
