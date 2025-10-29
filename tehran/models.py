from django.db import models


class tehran(models.Model):
    Area = models.FloatField()
    Room = models.IntegerField()
    Address = models.CharField(max_length=100)
    Parking = models.BooleanField(default=False)
    Warehouse = models.BooleanField(default=False)
    Elevator = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Address} - {self.Area}m² - {self.Room} Room  "
