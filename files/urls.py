from django.urls import path
from . import views

urlpatterns = [
    path('get_customer_files', views.get_customer_files, name='fetch_files'),
]
