from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _ 
from datetime import datetime

# Create your models here.

class Kategories(models.Model):
    author = models.CharField(max_length=85)
    kategorie=models.CharField(max_length=25)
   
    def __str__(self) -> str:
        return f"{self.kategorie}"
    
    
class weecklines(models.Model):
    author = models.CharField(max_length=85)
    week=models.IntegerField()
    line=models.CharField(max_length=89)
   
    def __str__(self) -> str:
        return f"W({self.week}):{self.line}"
    
class Task(models.Model):
    date =models.DateField(null=True)
    author = models.CharField(max_length=85)
    begin = models.TimeField()
    end=models.TimeField()
    task=models.CharField(max_length=89)
    classi= models.ForeignKey(Kategories,on_delete=models.CASCADE,related_name="tasks")
    
    def clean(self):
        super().clean()
        existing=Task.objects.filter(
           date=self.date,
           author=self.author
            ).exclude(pk=self.pk).filter(
            (
              models.Q(begin__lt=self.end, end__gt=self.begin) |
              models.Q(begin__lte=self.begin, end__gte=self.end) |
              models.Q(begin__lt=self.end, end__gte=self.end) |
              models.Q(begin__lte=self.begin, end__gt=self.begin)
            )
            )
        
        if existing.exists():
            raise ValidationError(_('An event already exists at this time on this date.'))
            
    def save(self, *args, **kwargs):
        self.full_clean()  # Run full clean before saving
        super().save(*args, **kwargs)
        
        
    def __str__(self) -> str:
        return f"{self.task}({self.begin}-{self.end})"



    
class dates(models.Model):
    author=models.CharField(max_length=85)
    date=models.DateField()
    actitivies = models.ManyToManyField(Task,blank=True,related_name="dates")
    
    def __str__(self) -> str:
        return f"{self.date}"