from django.db import models

# Create your models here.

class Forms(models.Model):
    FirstName = models.CharField(max_length=20)
    LastName = models.CharField(max_length=20)
    Address = models.CharField(max_length=20)
    Gender = models.CharField(max_length=6)
    Field = models.CharField(max_length=3)

    def __str__(self):
        return self.FirstName
    


class Image(models.Model):
    image = models.ImageField(upload_to='Forms/pdfs')