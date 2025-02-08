from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)
    index = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    index = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Ability(models.Model):
    name = models.CharField(max_length=50, unique=True)
    index = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.ManyToManyField("Skill", blank=True)

    def __str__(self):
        return self.full_name
