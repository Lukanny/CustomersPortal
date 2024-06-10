from django.urls import path
from django.contrib.auth import views as auth_views
from .views import dashboard, login, custom_logout, register, CustomPasswordResetView, CustomPasswordResetConfirmView

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('login', login, name='login'),
    path('logout', custom_logout, name='logout'),
    path('register', register, name='register'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/<uidb64>/<token>/password_reset_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
