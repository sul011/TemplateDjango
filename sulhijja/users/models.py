from django.db import models

from django.contrib.auth.models import User



class Datadiri(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telp = models.CharField(max_length=14)
    alamat = models.TextField()

    def __str__(self):
        return "{} - {}".format(self.user, self.telp)
        
    class Meta:
        verbose_name_plural ="Datadiri"
class API(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Api'

    def __str__(self):
        return self.user.username
 