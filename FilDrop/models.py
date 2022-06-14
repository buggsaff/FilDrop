from django.db import models

# Create your models here.
class User(models.Model):
    WalletAddress = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.WalletAddress
