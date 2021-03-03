from django.db import models
from django.utils import timezone

class NavigationInfo(models.Model):
    scope = models.CharField(max_length=150)
    level1 = models.CharField(max_length=150, blank=True, null=True)
    level2 = models.CharField(max_length=150, blank=True, null=True)
    level3 = models.CharField(max_length=150, blank=True, null=True)
    level4 = models.CharField(max_length=150, blank=True, null=True)
    level5 = models.CharField(max_length=150, blank=True, null=True)
    
class CalculationInfo(models.Model):
    ef = models.FloatField()
    cu = models.CharField(max_length=15)
    
class OtherInfo(models.Model):
    last_update = models.DateTimeField(default=timezone.now)
    preference = models.IntegerField()
    source = models.CharField(max_length=150)
      
class FlatfileEntry(models.Model):
    ref_num = models.IntegerField(default=0, primary_key=True)
    navigation_info = models.ForeignKey(NavigationInfo, on_delete=models.CASCADE)
    calculation_info = models.ForeignKey(CalculationInfo, on_delete=models.CASCADE)
    other_info = models.ForeignKey(OtherInfo, on_delete=models.CASCADE)