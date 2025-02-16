from django.contrib.sites import requests
from django.shortcuts import render
import requests

from main.forms import CharacterForm
from main.models import Character


def index(request):
    form = CharacterForm(request.POST or None)

    skills_list = []
    if form.is_valid():
        character = form.save(commit=False)
        # Вычисляем для каждого навыка бонус и признак владения
        for skill in Skill.objects.all():
            # Получаем модификатор характеристики для навыка
            ability_modifier = character.get_ability_modifier(skill.ability.full_name)
            # Если у персонажа есть background и он владеет этим навыком, добавляем +2
            if character.background and skill in character.background.skill_proficiencies.all():
                proficiency_bonus = 2
                owned = True
            else:
                proficiency_bonus = 0
                owned = False
            total_bonus = ability_modifier + proficiency_bonus

            skills_list.append({
                'name': skill.name,
                'ability': skill.ability_score.name,
                'bonus': total_bonus,
                'owned': owned,
            })
    context = {
        "title": "Редактирование персонажа",
        "form": form,
        "skills_list": skills_list,
    }
    return render(request, "index.html", context)
