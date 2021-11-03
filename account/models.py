from django.db import models


class Profile(models.Model):
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.email


class Customer(models.Model):
    name = models.CharField(max_length=200)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
