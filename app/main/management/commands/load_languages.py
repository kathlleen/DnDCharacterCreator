import requests
from django.core.management.base import BaseCommand
from main.models import Language

API_URL = "https://www.dnd5eapi.co/api/languages/"

class Command(BaseCommand):
    help = "Загружает языки DnD в базу данных"

    def handle(self, *args, **kwargs):
        response = requests.get(API_URL)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR("Ошибка загрузки данных"))
            return

        data = response.json().get("results", [])

        for item in data:
            language, created = Language.objects.get_or_create(
                index=item["index"],
                defaults={"name": item["name"]}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Добавлен язык: {language.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Язык уже существует: {language.name}"))

        self.stdout.write(self.style.SUCCESS("Загрузка языков завершена!"))
