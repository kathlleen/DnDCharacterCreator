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

class AbilityScore(models.Model):
    name = models.CharField(max_length=50, unique=True)
    index = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.ManyToManyField("Skill", blank=True)

    def __str__(self):
        return self.full_name

# class AbilityScore(models.Model):
#     index = models.CharField(max_length=50, unique=True)
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name

class Trait(models.Model):
    index = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Race(models.Model):
    index = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    speed = models.IntegerField(null=True, blank=True)
    alignment = models.TextField(null=True, blank=True)
    age = models.TextField(null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    size_description = models.TextField(null=True, blank=True)
    language_desc = models.TextField(null=True, blank=True)

    # Связи многие ко многим
    ability_bonuses = models.ManyToManyField(AbilityScore, through="RaceAbilityBonus")
    languages = models.ManyToManyField(Language, related_name="races")
    traits = models.ManyToManyField(Trait, related_name="races")

    def __str__(self):
        return self.name

class RaceAbilityBonus(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    ability_score = models.ForeignKey(AbilityScore, on_delete=models.CASCADE)
    bonus = models.IntegerField()

    class Meta:
        unique_together = ("race", "ability_score")

class Class(models.Model):
    index = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# class Subclass(models.Model):
#     index = models.CharField(max_length=50, unique=True)
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name


class Equipment(models.Model):
    index = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Proficiency(models.Model):
    index = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    classes = models.ManyToManyField(Class, related_name="proficiencies", blank=True)
    races = models.ManyToManyField(Race, related_name="proficiencies", blank=True)
    reference = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

#
# class MagicSchool(models.Model):
#     index = models.CharField(max_length=50, unique=True)
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
# class Spell(models.Model):
#     index = models.CharField(max_length=50, unique=True)
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     higher_level = models.TextField(blank=True, null=True)
#     range = models.CharField(max_length=50)
#     components = models.JSONField()
#     material = models.TextField(blank=True, null=True)
#     ritual = models.BooleanField()
#     duration = models.CharField(max_length=50)
#     concentration = models.BooleanField()
#     casting_time = models.CharField(max_length=50)
#     level = models.IntegerField()
#     attack_type = models.CharField(max_length=50, blank=True, null=True)
#     damage = models.JSONField(blank=True, null=True)
#     school = models.ForeignKey(MagicSchool, on_delete=models.CASCADE)
#     classes = models.ManyToManyField("Class", related_name="spells")
#     subclasses = models.ManyToManyField("Subclass", related_name="spells")
#
#     def __str__(self):
#         return self.name
