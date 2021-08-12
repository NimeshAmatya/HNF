from django.db import models

# Create your models here.
class Register(models.Model):
    FirstName = models.CharField(max_length=20)
    LastName = models.CharField(max_length=20)
    Username = models.CharField(max_length=20)
    Email = models.EmailField()
    Password = models.CharField(max_length=10)
    ConfirmPassword = models.CharField(max_length=10)

    def __str__(self):
        return self.FirstName

class Login(models.Model):
    Username = models.CharField(max_length=20)
    Password = models.CharField(max_length=10)

    def __str__(self):
        return self.Username
        