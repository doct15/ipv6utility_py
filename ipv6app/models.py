from django.db import models

class Prefix(models.Model):
    ip = models.CharField(max_length=128)
    mask = models.CharField(max_length=128, blank=True)
    name = models.CharField(max_length=128)
    possible = models.IntegerField(default=0)
    flag = models.CharField(max_length=128, blank=True)
    
    def __str__(self):
        return self.ip
