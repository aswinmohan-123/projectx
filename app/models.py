from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

class projectx_user(AbstractBaseUser):
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)

    def name(self, instance):
        return instance.first_name+' '+instance.last_name

