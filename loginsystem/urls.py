from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='login.home'),
    path('login/', Login, name='login.login' ),
]
