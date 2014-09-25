from django.db import models

# Create your models here.
class PortTarget(models.Model):
	sys_info = models.CharField(max_length=20)
	ip = models.CharField(max_length=20)


class Port(models.Model):
	target = models.ForeignKey(PortTarget)
	number = models.IntegerField()
	details = models.CharField(max_length=100)