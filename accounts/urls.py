from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib import admin
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Authentication Endpoints
    path('signup/', views.RegisterView.as_view(), name="signup"),
    path('login/', views.LoginViewUser.as_view(), name="login"),
    path('logout/', views.LogoutViewUser.as_view(), name="logout"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('profile/', views.profile, name="profile"),


    # change password
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/registration/password_change_done.html'), 
        name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/registration/password_change.html', success_url = reverse_lazy("password_change_done")), 
        name='password_change'),


    #Forgot password
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = "accounts/registration/password_reset_form.html", success_url = reverse_lazy("password_reset_complete")), 
    name="password_reset_confirm"),  # 3
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name = "accounts/registration/password_reset.html", success_url = reverse_lazy("password_reset_done"), email_template_name = 'accounts/registration/forgot_password_email.html'), 
    name="reset_password"),     # 1
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name = "accounts/registration/password_reset_sent.html"), 
    name="password_reset_done"),    # 2
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name = "accounts/registration/password_reset_done.html"), 
    name="password_reset_complete"),   # 4
    
]

