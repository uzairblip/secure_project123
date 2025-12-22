from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # This connects the address 'login/' to the visual login page
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
]