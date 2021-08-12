from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

app_name = "UMS"

urlpatterns = [
    path("", views.home,name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login,name="login"),
    path("accounts/login/",views.login, name="login"),
    path("logout/",views.logout, name="logout"),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="ums/password_reset.html"),
      name="password_reset"),

    path('reset_password_sent/', 
    auth_views.PasswordResetDoneView.as_view(template_name="ums/password_reset_sent.html"), 
    name="password_reset_done"),

    path('reset/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(template_name="ums/password_reset_form.html"), 
    name="password_reset_confirm"),

    path('reset_password_complete/', 
    auth_views.PasswordResetCompleteView.as_view(template_name="ums/password_reset_done.html"), 
    name="password_reset_complete"),
]