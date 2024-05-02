from django.urls import path
from . import views

urlpatterns = [
    path('<int:file_id>', views.fetch_file, name='fetch_file'),
]
