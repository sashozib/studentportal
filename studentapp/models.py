from django.db import models

# Create your models here.

shift_choose = [
    ("1st", "Frist Shift"),
    ("2nd", "Second Shift")
]

class Student(models.Model):
    name = models.CharField(max_length=50)
    roll = models.IntegerField(primary_key=True, null=False, blank=False, unique=True)
    birth_date = models.DateField(null=False)
    shift = models.CharField(max_length=4, choices=shift_choose)
    session = models.CharField(max_length=15)
    
    def __str__(self) -> str:
        return str(self.roll)