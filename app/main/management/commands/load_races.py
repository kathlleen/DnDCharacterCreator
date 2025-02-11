import requests
from django.core.management.base import BaseCommand
from main.models import Race, AbilityScore, Language, Trait, RaceAbilityBonus

API_URL = "https://www.dnd5eapi.co/api/races/"

class Command(BaseCommand):
    help = "Загружает расы в базу данных"

    def handle(self, *args, **kwargs):
        response = requests.get(API_URL)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR("Ошибка загрузки данных"))
            return

        races = response.json().get("results", [])

        for race_data in races:
            race_info = requests.get(f"{API_URL}{race_data['index']}").json()

            race, created = Race.objects.get_or_create(
                index=race_info["index"],
                defaults={
                    "name": race_info["name"],
                    "speed": race_info["speed"],
                    "alignment": race_info["alignment"],
                    "age": race_info["age"],
                    "size": race_info["size"],
                    "size_description": race_info["size_description"],
                    "language_desc": race_info["language_desc"],
                },
            )

            # Добавляем бонусы к характеристикам
            for ability_bonus in race_info["ability_bonuses"]:
                ability, _ = AbilityScore.objects.get_or_create(
                    index=ability_bonus["ability_score"]["index"],
                    defaults={"name": ability_bonus["ability_score"]["name"]}
                )
                RaceAbilityBonus.objects.get_or_create(
                    race=race, ability_score=ability, bonus=ability_bonus["bonus"]
                )

            # Добавляем языки
            for language_data in race_info["languages"]:
                language, _ = Language.objects.get_or_create(
                    index=language_data["index"],
                    defaults={"name": language_data["name"]}
                )
                race.languages.add(language)

            # Добавляем черты расы
            for trait_data in race_info["traits"]:
                trait, _ = Trait.objects.get_or_create(
                    index=trait_data["index"],
                    defaults={"name": trait_data["name"]}
                )
                race.traits.add(trait)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Добавлена раса: {race.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Раса уже существует: {race.name}"))

        self.stdout.write(self.style.SUCCESS("Загрузка рас завершена!"))
