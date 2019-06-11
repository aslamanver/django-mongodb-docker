from django.urls import path, include
from . import views

urlpatterns = [
    
    path('home/', views.home),
    path('edit/<str:oid>/', views.edit),

    path('entrance/', views.entrance, name='entrance')
]
