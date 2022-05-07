from email.policy import default
from django.db import models

# Create your models here.


class Region_lan(models.Model):
    region=models.CharField(max_length=200)
    language=models.CharField(max_length=200, default="")
    sample_texts=models.TextField(default="Type in some texts here to convert to voices")
    
    def __str__(self):
        return f"{self.language}"

class Voice(models.Model):
    voice_region=models.ForeignKey(Region_lan,on_delete=models.CASCADE)
    voice_person=models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.voice_region} by {self.voice_person} "