from django.contrib import admin

from main.models import Language, Skill,Ability
# Register your models here.
admin.site.register(Language)
admin.site.register(Skill)
admin.site.register(Ability)
# admin.site.register(Proficiency)