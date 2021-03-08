from django.db import models

# Create your models here.

#Our model will only need to store a city name and pass this information to the API request

class City(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
