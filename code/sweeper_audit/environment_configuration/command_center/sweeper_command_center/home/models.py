from django.db import models
# Create your models here.
class Total(models.Model):
    vehicle_id = models.CharField('VehicleID', max_length=64)
    company = models.CharField('Company', max_length=64)
    currentdate = models.CharField('CurrentDate', max_length=64,default='09-05-2022')
    currenttime = models.CharField('CurrentTime', max_length=64,default='14-51-23')
    road = models.CharField('Road', max_length=64, default='NanyangLink')
    suburb = models.CharField('Suburb', max_length=64, default='JurongWest')
    county = models.CharField('County', max_length=64, default='Pioneer')
    postcode = models.IntegerField('Postcode', default=0)
    avg_unclean_level = models.IntegerField('AvgUncleanLevel', default=0)
    duration = models.IntegerField('Duration', default=0)
    latitude = models.FloatField('Latitude', default=1.3422035)
    longitude = models.FloatField('Longitude', default=103.681429)

