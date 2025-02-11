import requests
from django.core.management.base import BaseCommand
from main.models import Skill
from main.models import AbilityScore

API_URL = "https://www.dnd5eapi.co/api/ability-scores/"

class Command(BaseCommand):
    help = "Загружает характеристики (abilities) в базу данных"

    def handle(self, *args, **kwargs):
        response = requests.get(API_URL)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR("Ошибка загрузки данных"))
            return

        data = response.json().get("results", [])

        for item in data:
            ability_data = requests.get(f"{API_URL}{item['index']}").json()
            description = " ".join(ability_data.get("desc", []))

            ability, created = AbilityScore.objects.get_or_create(
                index=item["index"],
                defaults={
                    "name": item["name"],
                    "full_name": ability_data["full_name"],
                    "description": description,
                },
            )

            # Привязываем навыки (если они есть)
            skill_list = ability_data.get("skills", [])
            for skill_info in skill_list:
                skill, _ = Skill.objects.get_or_create(index=skill_info["index"], defaults={"name": skill_info["name"]})
                ability.skills.add(skill)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Добавлена характеристика: {ability.full_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Характеристика уже существует: {ability.full_name}"))

        self.stdout.write(self.style.SUCCESS("Загрузка характеристик завершена!"))
