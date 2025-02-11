import requests
from django.core.management.base import BaseCommand
from main.models import Skill

API_URL = "https://www.dnd5eapi.co/api/skills/"


class Command(BaseCommand):
    help = "Загружает навыки DnD в базу данных"

    def handle(self, *args, **kwargs):
        response = requests.get(API_URL)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR("Ошибка загрузки данных"))
            return

        data = response.json().get("results", [])

        for item in data:
            skill_data = requests.get(f"{API_URL}{item['index']}").json()
            description = " ".join(skill_data.get("desc", []))  # Описание может быть списком строк

            skill, created = Skill.objects.get_or_create(
                index=item["index"],
                defaults={"name": item["name"], "description": description}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Добавлен навык: {skill.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Навык уже существует: {skill.name}"))

        self.stdout.write(self.style.SUCCESS("Загрузка навыков завершена!"))
