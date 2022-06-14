from django.urls import path
from FilDrop.views import *

urlpatterns = [
    path('',Home,name='home'),
    path('login/',Login,name='login'),
    path('user/',UserPage, name='userpage'),
    path('addCollection/',AddCollection,name='addCollection'),
    path('imageUpload/<int:pkk>/',ImageUpload,name='imageUpload'),
    path('deploy/<str:collectionname>/',Deploy,name='deploy')
]
