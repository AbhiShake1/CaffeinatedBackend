from django.urls import path

from .views import SignupView, LoginView, LogoutView, ResetPasswordView, SendPasswordResetLinkView, ChangePasswordView

urlpatterns = [
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset-password/<str:uidb64>/<str:token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('send-reset-link/', SendPasswordResetLinkView.as_view(), name='send_reset_link'),
]
