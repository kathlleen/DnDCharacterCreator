from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models

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

    ability_bonuses = models.ManyToManyField(AbilityScore, through="RaceAbilityBonus")
    languages = models.ManyToManyField(Language, related_name="races")
    traits = models.ManyToManyField(Trait, related_name="races")
    proficiencies = models.ManyToManyField("Proficiency", related_name="races_with_proficiency", blank=True)

    def __str__(self):
        return self.name


class RaceAbilityBonus(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    ability_score = models.ForeignKey(AbilityScore, on_delete=models.CASCADE)
    bonus = models.IntegerField()

    class Meta:
        unique_together = ("race", "ability_score")


class Equipment(models.Model):
    index = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True)
    weight = models.FloatField(null=True, blank=True)
    cost = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name


class CharacterClass(models.Model):
    index = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    hit_die = models.IntegerField()
    proficiencies = models.ManyToManyField("Proficiency", related_name="character_classes_with_proficiency", blank=True)
    saving_throws = models.ManyToManyField("AbilityScore", related_name="saving_throws", blank=True)
    starting_equipment = models.ManyToManyField("Equipment", through="StartingEquipment", blank=True)

    def __str__(self):
        return self.name


class Proficiency(models.Model):
    index = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=[("armor", "Armor"), ("weapon", "Weapon"), ("skill", "Skill"), ("saving_throw", "Saving Throw")])
    classes = models.ManyToManyField("CharacterClass", related_name="proficiencies_for_classes", blank=True)
    races = models.ManyToManyField("Race", related_name="proficiencies_for_races", blank=True)
    reference = models.ForeignKey("Equipment", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class ProficiencyChoice(models.Model):
    character_class = models.ForeignKey("CharacterClass", on_delete=models.CASCADE, related_name="proficiency_choices")
    num_choices = models.IntegerField(default=1)
    options = models.ManyToManyField("Proficiency", related_name="proficiency_options")

    def __str__(self):
        return f"{self.character_class.name}: Choose {self.num_choices} proficiencies"


class StartingEquipment(models.Model):
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class EquipmentChoice(models.Model):
    description = models.TextField()
    character_class = models.ForeignKey("CharacterClass", on_delete=models.CASCADE, related_name="equipment_choices")
    options = models.ManyToManyField("Equipment", related_name="equipment_options")

    def __str__(self):
        return f"Choice for {self.character_class.name}: {self.description}"

from django.db import models

class Background(models.Model):
    index = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    skill_proficiencies = models.ManyToManyField("Skill", related_name="backgrounds_with_skills", blank=True)
    tool_proficiencies = models.TextField(blank=True, null=True)
    language_options = models.IntegerField(default=0, help_text="Количество языков, которые можно выбрать")
    starting_equipment = models.TextField(blank=True, null=True)
    feature_name = models.CharField(max_length=100, blank=True, null=True)
    feature_description = models.TextField(blank=True, null=True)

    gold = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Кастомная модель пользователя, расширяющая стандартную Django User"""
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    def __str__(self):
        return self.username

class Character(models.Model):
    """Модель персонажа"""
    # image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Avatar')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="characters")
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    character_class = models.ForeignKey(CharacterClass, on_delete=models.SET_NULL, null=True, blank=True)
    race = models.ForeignKey(Race, on_delete=models.SET_NULL, null=True, blank=True)
    background = models.ForeignKey(Background, on_delete=models.SET_NULL, null=True, blank=True)

    strength = models.IntegerField(default=10)
    dexterity = models.IntegerField(default=10)
    constitution = models.IntegerField(default=10)
    intelligence = models.IntegerField(default=10)
    wisdom = models.IntegerField(default=10)
    charisma = models.IntegerField(default=10)

    hit_points = models.IntegerField(default=10)
    armor_class = models.IntegerField(default=10)
    speed = models.IntegerField(default=30)

    gold = models.IntegerField(default=0)

    skills = models.ManyToManyField(Skill, blank=True)
    equipment = models.TextField(blank=True)
    traits = models.ManyToManyField(Trait, blank=True)
    languages = models.ManyToManyField(Language, blank=True)
    proficiencies = models.ManyToManyField(Proficiency, blank=True)

    def __str__(self):
        return f"{self.name} (Lvl {self.level})"

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
