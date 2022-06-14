from django.contrib import admin
from FilDrop.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(UserCollection)
admin.site.register(UserCollectionImage)