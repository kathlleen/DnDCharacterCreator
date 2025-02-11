import requests
from django.core.management.base import BaseCommand
from main.models import Proficiency, Class, Race, Equipment

API_URL = "https://www.dnd5eapi.co/api/proficiencies/"

class Command(BaseCommand):
    help = "Загружает владения в базу данных"

    def handle(self, *args, **kwargs):
        response = requests.get(API_URL)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR("Ошибка загрузки данных"))
            return

        proficiencies = response.json().get("results", [])

        for proficiency_data in proficiencies:
            proficiency_info = requests.get(f"{API_URL}{proficiency_data['index']}").json()

            reference = None
            if "reference" in proficiency_info:
                reference, _ = Equipment.objects.get_or_create(
                    index=proficiency_info["reference"]["index"],
                    defaults={"name": proficiency_info["reference"]["name"]}
                )

            proficiency, created = Proficiency.objects.get_or_create(
                index=proficiency_info["index"],
                defaults={
                    "name": proficiency_info["name"],
                    "type": proficiency_info["type"],
                    "reference": reference,
                },
            )

            # Привязываем классы
            for class_data in proficiency_info.get("classes", []):
                class_obj, _ = Class.objects.get_or_create(index=class_data["index"], defaults={"name": class_data["name"]})
                proficiency.classes.add(class_obj)

            # Привязываем расы
            for race_data in proficiency_info.get("races", []):
                race_obj, _ = Race.objects.get_or_create(index=race_data["index"], defaults={"name": race_data["name"]})
                proficiency.races.add(race_obj)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Добавлено владение: {proficiency.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Владение уже существует: {proficiency.name}"))

        self.stdout.write(self.style.SUCCESS("Загрузка владений завершена!"))
