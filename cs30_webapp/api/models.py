from django.db import models

class FlatfileEntry(models.Model):
    #For now just sample info
    title = models.CharField(max_length=70, blank=False, default='')