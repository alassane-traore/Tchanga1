from django.db import models
from django.forms import ValidationError

# Create your models here.


class Sector(models.Model):
    author=models.CharField(max_length=89)
    name=models.CharField(max_length=59)
    begin=models.DateTimeField()
    end=models.DateTimeField()
    budget=models.FloatField(editable=True)
    
    automate=models.BooleanField(default=True,editable=True)
    def clean(self):
        super().clean()
        existing=Sector.objects.filter(
           name=self.name,
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
            #return print('An event already exists at this time on this date.')
            raise ValidationError(f"An event already exists for {self.begin} to {self.end}")
           
    def save(self, *args, **kwargs):
        self.full_clean()  # Run full clean before saving
        super().save(*args, **kwargs)
            
    def __str__(self) -> str:
        return f"{self.name}({self.begin}-{self.end})"

class Goods(models.Model):
    author =models.CharField(max_length=89)
    #d = models.DateTimeField()
    s = models.ForeignKey(Sector,on_delete=models.CASCADE,related_name="goods",null=True)
    name=models.CharField(max_length=69)
    booked=models.BooleanField(default=False,editable=True)
    
    def __str__(self) -> str:
        return f"{self.s}:{self.name} Booked:{self.booked}"

class Basket(models.Model):
    author =models.CharField(max_length=89)
    d = models.DateTimeField()
    costs=models.FloatField(editable=True)
    comment=models.CharField(max_length=205,null=True,blank=True)
    kaufliste=models.ManyToManyField(Goods,related_name="busket",blank=True)
    sector=models.ForeignKey(Sector,on_delete=models.CASCADE,related_name="buskets",null=True)
    def __str__(self) -> str:
        return f"{self.d}:({self.kaufliste})"

    