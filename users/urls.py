from django.urls import path
from users.views import (
    GenerateAuthToken,
    ConfirmLogin,
    Logout,
    NewRegistrationsView,
    ChangePasswordView,
    ChangeEmailView

)

urlpatterns = [
    path("login/", GenerateAuthToken.as_view(), name="get-token"),
    path("confirm_login/", ConfirmLogin.as_view(), name="confirm-login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("register/", NewRegistrationsView.as_view(), name="register"),
    path('change_password/', ChangePasswordView.as_view(), name='password-change'),
    path('change_email/', ChangeEmailView.as_view(), name='change-email')

]
