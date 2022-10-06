from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models


class ParkingSpace(models.Model):
    parking_address = models.CharField(max_length=5)
    availability = models.BooleanField(default=True)
    in_process = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    vehicle_id = models.CharField(max_length=6, blank=True)



        