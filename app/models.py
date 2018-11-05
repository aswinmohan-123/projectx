from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

class projectx_user(AbstractBaseUser):
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'

    def name(self, instance):
        return instance.first_name+' '+instance.last_name

    def __str__(self):
        return self.username

class message(models.Model):
    from_user = models.ForeignKey('projectx_user', related_name='fromuser', on_delete=models.CASCADE)
    to_user = models.ForeignKey('projectx_user', related_name='touser', on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)

