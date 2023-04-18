from django.db import models


class Employee(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    position = models.CharField(max_length=64)
    experience = models.IntegerField(help_text="Number of years working in the company")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Room(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.IntegerField()
