from django.db import models

# Create your models here.
class Race(models.Model):
    index = models.CharField(max_length=50, blank = True, null = True)
    name = models.CharField(max_length=50, blank = True, null = True)
    speed = models.IntegerField(blank=True, null=True)
    age = models.CharField(max_length=150, blank = True, null = True)
    alignment = models.TextField(max_length=150, blank = True, null = True)
    size = models.CharField(max_length=20, blank = True, null = True)
    size_description = models.TextField(max_length=150, blank = True, null = True)
    languages = models.CharField(max_length=150, blank = True, null = True)
    language_desc = models.TextField(max_length=150, blank = True, null = True)
    traits = models.TextField(max_length=150, blank = True, null = True)

    def __str__(self):
        return self.name