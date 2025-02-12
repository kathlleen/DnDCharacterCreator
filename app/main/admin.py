from django.contrib import admin

from main.models import Language, Skill, Race, CharacterClass, Equipment, Proficiency, RaceAbilityBonus, \
    AbilityScore, Trait, StartingEquipment, EquipmentChoice
# Register your models here.
admin.site.register(Language)
admin.site.register(Skill)
# admin.site.register(Race)
# admin.site.register(CharacterClass)
admin.site.register(Equipment)
admin.site.register(Proficiency)
admin.site.register(AbilityScore)
admin.site.register(Trait)
admin.site.register(StartingEquipment)
# admin.site.register(StartingEquipment)
admin.site.register(EquipmentChoice)
# admin.site.register(RaceAbilityBonus)

class RaceAbilityBonusInline(admin.TabularInline):  # Можно заменить на StackedInline для другого вида
    model = RaceAbilityBonus
    extra = 1  # Количество пустых полей для добавления новых записей

# Админка для Race с Inline
@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ("name", "speed", "size")  # Поля, отображаемые в списке
    inlines = [RaceAbilityBonusInline]  # Вставляем связь RaceAbilityBonus

class StartingEquipmentInline(admin.TabularInline):  # Можно заменить на StackedInline для другого вида
    model = StartingEquipment
    extra = 1  # Количество пустых полей для добавления новых записей

@admin.register(CharacterClass)
class CharacterClassAdmin(admin.ModelAdmin):
    list_display = ("name",)  # Поля, отображаемые в списке
    inlines = [StartingEquipmentInline]  # Вставляем связь RaceAbilityBonus

# admin.site.register(Spell)
# admin.site.register(Subclass)