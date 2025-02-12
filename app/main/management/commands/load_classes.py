import requests
from django.core.management.base import BaseCommand
from main.models import CharacterClass, Proficiency, AbilityScore, Equipment, StartingEquipment, ProficiencyChoice, \
    EquipmentChoice


class Command(BaseCommand):
    help = 'Загружает классы из API DnD 5e и сохраняет их в базу данных'

    def get_class_data(self, index):
        """Получить данные о классе из API"""
        url = f"https://www.dnd5eapi.co/api/classes/{index}"
        response = requests.get(url)
        return response.json()

    def load_class(self, index):
        """Загружает данные конкретного класса и сохраняет их в базу данных"""
        class_data = self.get_class_data(index)

        # Создаем или находим класс в базе
        character_class, created = CharacterClass.objects.get_or_create(
            index=class_data['index'],
            defaults={'name': class_data['name'], 'hit_die': class_data['hit_die']}
        )
        self.stdout.write(self.style.SUCCESS(f"Класс {character_class.name} {'создан' if created else 'обновлен'}"))

        # Заполняем proficiencies (профессии)
        for proficiency_data in class_data['proficiencies']:
            proficiency, created = Proficiency.objects.get_or_create(
                index=proficiency_data['index'],
                defaults={'name': proficiency_data['name']}
            )
            character_class.proficiencies.add(proficiency)

        # Заполняем saving_throws (спасброски)
        for saving_throw_data in class_data['saving_throws']:
            ability_score, created = AbilityScore.objects.get_or_create(
                index=saving_throw_data['index'],
                defaults={'name': saving_throw_data['name']}
            )
            character_class.saving_throws.add(ability_score)

        # Заполняем starting equipment (начальное снаряжение)
        for equipment_data in class_data['starting_equipment']:
            equipment, created = Equipment.objects.get_or_create(
                index=equipment_data['equipment']['index'],
                defaults={'name': equipment_data['equipment']['name']}
            )
            StartingEquipment.objects.create(
                character_class=character_class,
                equipment=equipment,
                quantity=equipment_data.get('quantity', 1)
            )

        # Заполняем starting_equipment_options (выбор снаряжения)
        for choice_data in class_data['starting_equipment_options']:
            equipment_choice = EquipmentChoice.objects.create(
                description=choice_data['desc'],
                character_class=character_class
            )

            # Проверяем, есть ли ключ 'from' и обрабатываем его
            if 'from' in choice_data:
                options_data = choice_data['from'].get('options', [])

                for option_data in options_data:
                    # Если 'of' есть, добавляем снаряжение
                    if 'of' in option_data:
                        equipment, created = Equipment.objects.get_or_create(
                            index=option_data['of']['index'],
                            defaults={'name': option_data['of']['name']}
                        )
                        equipment_choice.options.add(equipment)

                    # Если есть 'prerequisites', обрабатываем их отдельно
                    if 'prerequisites' in option_data:
                        for prerequisite in option_data['prerequisites']:
                            if prerequisite['type'] == 'proficiency':
                                proficiency, created = Proficiency.objects.get_or_create(
                                    index=prerequisite['proficiency']['index'],
                                    defaults={'name': prerequisite['proficiency']['name']}
                                )
                                # Здесь можно добавить логику работы с proficiency, если нужно
                                # Например, связываем proficiency с выбором снаряжения
                                # equipment_choice.proficiencies.add(proficiency)  # Это можно использовать, если нужно.

                    # Если есть дополнительные условия, их можно добавить здесь
                    if 'option_type' in option_data and option_data['option_type'] == 'counted_reference':
                        equipment, created = Equipment.objects.get_or_create(
                            index=option_data['of']['index'],
                            defaults={'name': option_data['of']['name']}
                        )
                        equipment_choice.options.add(equipment)

        # Заполняем proficiency choices (выбор профiciencies)
        for proficiency_choice_data in class_data['proficiency_choices']:
            proficiency_choice = ProficiencyChoice.objects.create(
                character_class=character_class,
                num_choices=proficiency_choice_data['choose']
            )

            if 'from' in proficiency_choice_data and 'options' in proficiency_choice_data['from']:
                for option_data in proficiency_choice_data['from']['options']:
                    if 'option_type' in option_data and option_data['option_type'] == 'reference':
                        # Проверяем, есть ли ключ 'item' и получаем данные о профиците
                        if 'item' in option_data:
                            proficiency, created = Proficiency.objects.get_or_create(
                                index=option_data['item']['index'],
                                defaults={'name': option_data['item']['name']}
                            )
                            proficiency_choice.options.add(proficiency)

        self.stdout.write(self.style.SUCCESS(f"Класс {character_class.name} успешно загружен!"))

    def handle(self, *args, **kwargs):
        """Главная логика команды"""
        classes = ['barbarian', 'bard', 'cleric', 'druid', 'fighter', 'monk',
                   'paladin', 'ranger', 'rogue', 'sorcerer', 'warlock', 'wizard']  # Список индексов классов, которые нужно загрузить (можно добавить другие)

        for class_index in classes:
            self.load_class(class_index)

        self.stdout.write(self.style.SUCCESS('Все классы успешно загружены!'))
