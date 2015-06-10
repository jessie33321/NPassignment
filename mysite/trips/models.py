from django.db import models

# Create your models here.
class info(models.Model):
	name = models.CharField(max_length=100)
	gender = models.CharField(max_length=100)
	height = models.CharField(max_length=100)
	weight = models.CharField(max_length=100)
	time = models.CharField(max_length=100)
	
	def __str__(self):
		return self.name
		
class account(models.Model):
	name = models.CharField(max_length=100)
	password = models.CharField(max_length=100)