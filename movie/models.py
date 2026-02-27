from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=100)  #nombre
    description = models.CharField(max_length=250)  #descripcion
    image = models.ImageField(upload_to='movie/images/')  #imagen
    url = models.URLField(blank=True)  #link
    genre = models.CharField(max_length=50, blank=True)  #género
    year = models.IntegerField(null=True, blank=True)  #año de la película
