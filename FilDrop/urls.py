from django.urls import path
from FilDrop.views import Home

urlpatterns = [
    path('',Home,name='home')
]
