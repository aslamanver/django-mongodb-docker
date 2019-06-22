from django.urls import path, include
from . import views

urlpatterns = [
    
    # Signup Start 
    path('signup/a', views.signup_a, name = 'signup_a'),
    path('signup/email_verify', views.signup_email_verify, name = 'signup_email_verify')

]