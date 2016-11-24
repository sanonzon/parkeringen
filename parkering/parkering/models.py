from django.db import models
from django.contrib.auth.models import User


class Parkspace(models.Model):
	number = models.IntegerField(unique=True)
	available = models.BooleanField(default=False)
	avail_start = models.DateField(blank=True,null=True)
	avail_end = models.DateField(blank=True,null=True)
	
	def __str__(self):
		avail = " - Available" if self.available else ""
		return str("%s %s"%(self.number,avail))
	
class User_Extended(models.Model):
	#~ id = models.ForeignKey(User,on_delete=models.CASCADE,primary_key=True)
	username = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
	phone = models.CharField(max_length=20,blank=True)
	own_space = models.ForeignKey(Parkspace, on_delete=models.CASCADE,blank=True)

	def __str__(self):
		return self.name
