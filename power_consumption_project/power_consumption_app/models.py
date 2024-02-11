from django.db import models

class data(models.Model):
    power = models.CharField(max_length=7)
    voltage = models.CharField(max_length=7)
    current = models.CharField(max_length=7)
    electricity = models.CharField(max_length=7)
    timestamp = models.CharField(max_length=100)

    def __str__(self):
        return self.power + ' - ' + self.voltage + ' - ' + self.current
     
