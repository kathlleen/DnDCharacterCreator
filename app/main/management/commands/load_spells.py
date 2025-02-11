import requests
from django.core.management.base import BaseCommand
from main.models import Spell, MagicSchool, Class, Subclass

API_URL = "https://www.dnd5eapi.co/api/spells/"

class Command(BaseCommand):
    help = "Загружает заклинания в базу данных"

    def handle(self, *args, **kwargs):
        response = requests.get(API_URL)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR("Ошибка загрузки данных"))
            return

        spells = response.json().get("results", [])

        for spell_data in spells:
            spell_info = requests.get(f"{API_URL}{spell_data['index']}").json()

            school, _ = MagicSchool.objects.get_or_create(
                index=spell_info["school"]["index"],
                defaults={"name": spell_info["school"]["name"]},
            )

            spell, created = Spell.objects.get_or_create(
                index=spell_info["index"],
                defaults={
                    "name": spell_info["name"],
                    "description": " ".join(spell_info.get("desc", [])),
                    "higher_level": " ".join(spell_info.get("higher_level", [])),
                    "range": spell_info["range"],
                    "components": spell_info["components"],
                    "material": spell_info.get("material", ""),
                    "ritual": spell_info["ritual"],
                    "duration": spell_info["duration"],
                    "concentration": spell_info["concentration"],
                    "casting_time": spell_info["casting_time"],
                    "level": spell_info["level"],
                    "attack_type": spell_info.get("attack_type", ""),
                    "damage": spell_info.get("damage", {}),
                    "school": school,
                },
            )

            # Привязываем классы
            for class_data in spell_info.get("classes", []):
                class_obj, _ = Class.objects.get_or_create(index=class_data["index"], defaults={"name": class_data["name"]})
                spell.classes.add(class_obj)

            # Привязываем подклассы
            for subclass_data in spell_info.get("subclasses", []):
                subclass_obj, _ = Subclass.objects.get_or_create(index=subclass_data["index"], defaults={"name": subclass_data["name"]})
                spell.subclasses.add(subclass_obj)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Добавлено заклинание: {spell.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Заклинание уже существует: {spell.name}"))

        self.stdout.write(self.style.SUCCESS("Загрузка заклинаний завершена!"))
