from django.contrib import admin

from main.models import Language, Skill, Race, Class, Equipment, Proficiency, RaceAbilityBonus, \
    AbilityScore, Trait
# Register your models here.
admin.site.register(Language)
admin.site.register(Skill)
# admin.site.register(Race)
admin.site.register(Class)
admin.site.register(Equipment)
admin.site.register(Proficiency)
admin.site.register(AbilityScore)
admin.site.register(Trait)
# admin.site.register(RaceAbilityBonus)

class RaceAbilityBonusInline(admin.TabularInline):  # Можно заменить на StackedInline для другого вида
    model = RaceAbilityBonus
    extra = 1  # Количество пустых полей для добавления новых записей

# Админка для Race с Inline
@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ("name", "speed", "size")  # Поля, отображаемые в списке
    inlines = [RaceAbilityBonusInline]  # Вставляем связь RaceAbilityBonus

# admin.site.register(Spell)
# admin.site.register(Subclass)