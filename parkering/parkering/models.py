from django.db import models


class Parkspace(models.Model):
    available = models.BooleanField()
    avail_start = models.DateField()
    avail_end = models.DateField()

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    own_space = models.ForeignKey(Parkspace, on_delete=models.CASCADE)

    def __str__(self):
        return self.name