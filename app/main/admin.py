from django.contrib import admin

from main.models import Language, Skill, Ability, Race, Class, Equipment, Proficiency
# Register your models here.
admin.site.register(Language)
admin.site.register(Skill)
admin.site.register(Ability)
admin.site.register(Race)
admin.site.register(Class)
admin.site.register(Equipment)
admin.site.register(Proficiency)
# admin.site.register(Spell)
# admin.site.register(Subclass)