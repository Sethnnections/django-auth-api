# myproject/urls.py

from django.urls import path
from users_auth.views import UserRegistration, UserLogin, UserProfile, UpdateProfile

urlpatterns = [
    path("register/", UserRegistration.as_view(), name="register"),
    path("login/", UserLogin.as_view(), name="login"),
    path("profile/", UserProfile.as_view(), name="profile"),
    path("update-profile/", UpdateProfile.as_view(), name="update_profile"),
]
