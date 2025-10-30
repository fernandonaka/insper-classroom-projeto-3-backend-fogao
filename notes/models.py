
# Create your models here.
from django.db import models
from django.db.models.functions import Lower

    
class Tag(models.Model):
    title = models.CharField(max_length=40, unique=True, null=True)

class Note(models.Model):
    title = models.CharField(max_length=200)
    content= models.TextField()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return(f'{self.id}.{self.title}')