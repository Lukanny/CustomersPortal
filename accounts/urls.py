from django.urls import path
from django.contrib.auth import views as auth_views
from .views import dashboard, login, custom_logout, change_user_info, register, CustomPasswordResetView, CustomPasswordResetConfirmView, activate

urlpatterns = [
    path('painel', dashboard, name='dashboard'),
    path('entrar', login, name='login'),
    path('sair', custom_logout, name='logout'),
    path('cadastro', register, name='register'),
    path('alterar_dados', change_user_info, name='edit'),
    path('redefinir_senha/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('redefinir_senha/feito/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('redefinir/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('redefinir/<uidb64>/<token>/senha_redefinida', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('activate/', activate, name='activate'),
]
