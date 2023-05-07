from datetime import datetime

from django.core.validators import MinValueValidator
from django.db import models

from api.settings import YEAR_IN_DAYS


class Employee(models.Model):
    POSITIONS = [
        ("manager", "Manager"),
        ("senior_developer", "Senior Developer"),
        ("developer", "Developer"),
        ("junior_developer", "Junior Developer"),
        ("designer", "Designer"),
        ("tester", "Tester"),
    ]

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    position = models.CharField(max_length=64, choices=POSITIONS)
    experience = models.IntegerField(validators=[MinValueValidator(0)], help_text="Number of years working in the company")
    date_of_birth = models.DateField(default=datetime.today().date())

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self) -> int:
        today = datetime.today().date()
        return (today - self.date_of_birth).days // YEAR_IN_DAYS


class Room(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.IntegerField()


class Reservation(models.Model):
    reserved_from = models.DateTimeField(default=datetime.now())
    reserved_to = models.DateTimeField(default=datetime.now())
    room = models.ForeignKey(Room, related_name="reservations", on_delete=models.CASCADE)
    host = models.ForeignKey(Employee, related_name="hosted_reservations", null=True, blank=True, on_delete=models.SET_NULL)
    attendees = models.ManyToManyField(Employee, related_name="attended_reservations")
