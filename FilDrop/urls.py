from django.urls import path
from FilDrop.views import *

urlpatterns = [
    path('',Home,name='home'),
    path('login/',Login,name='login')
]
