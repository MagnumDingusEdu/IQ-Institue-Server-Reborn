from django.urls import path
from users.views import GenerateAuthToken, ConfirmLogin, Logout

urlpatterns = [
    path("login/", GenerateAuthToken.as_view(), name="get-token"),
    path("confirm_login/", ConfirmLogin.as_view(), name="confirm-login"),
    path("logout/", Logout.as_view(), name="logout"),
]
