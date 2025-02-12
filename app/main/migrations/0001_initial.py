# Generated by Django 4.2.14 on 2025-02-12 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AbilityScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('index', models.CharField(max_length=10, unique=True)),
                ('full_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CharacterClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('hit_die', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(blank=True, max_length=50)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('cost', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('index', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proficiency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('armor', 'Armor'), ('weapon', 'Weapon'), ('skill', 'Skill'), ('saving_throw', 'Saving Throw')], max_length=100)),
                ('classes', models.ManyToManyField(blank=True, related_name='proficiencies_for_classes', to='main.characterclass')),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('speed', models.IntegerField(blank=True, null=True)),
                ('alignment', models.TextField(blank=True, null=True)),
                ('age', models.TextField(blank=True, null=True)),
                ('size', models.CharField(blank=True, max_length=50, null=True)),
                ('size_description', models.TextField(blank=True, null=True)),
                ('language_desc', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('index', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Trait',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StartingEquipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('character_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.characterclass')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.equipment')),
            ],
        ),
        migrations.CreateModel(
            name='RaceAbilityBonus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus', models.IntegerField()),
                ('ability_score', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.abilityscore')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.race')),
            ],
            options={
                'unique_together': {('race', 'ability_score')},
            },
        ),
        migrations.AddField(
            model_name='race',
            name='ability_bonuses',
            field=models.ManyToManyField(through='main.RaceAbilityBonus', to='main.abilityscore'),
        ),
        migrations.AddField(
            model_name='race',
            name='languages',
            field=models.ManyToManyField(related_name='races', to='main.language'),
        ),
        migrations.AddField(
            model_name='race',
            name='proficiencies',
            field=models.ManyToManyField(blank=True, related_name='races_with_proficiency', to='main.proficiency'),
        ),
        migrations.AddField(
            model_name='race',
            name='traits',
            field=models.ManyToManyField(related_name='races', to='main.trait'),
        ),
        migrations.CreateModel(
            name='ProficiencyChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_choices', models.IntegerField(default=1)),
                ('character_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proficiency_choices', to='main.characterclass')),
                ('options', models.ManyToManyField(related_name='proficiency_options', to='main.proficiency')),
            ],
        ),
        migrations.AddField(
            model_name='proficiency',
            name='races',
            field=models.ManyToManyField(blank=True, related_name='proficiencies_for_races', to='main.race'),
        ),
        migrations.AddField(
            model_name='proficiency',
            name='reference',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.equipment'),
        ),
        migrations.CreateModel(
            name='EquipmentChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('character_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipment_choices', to='main.characterclass')),
                ('options', models.ManyToManyField(related_name='equipment_options', to='main.equipment')),
            ],
        ),
        migrations.AddField(
            model_name='characterclass',
            name='proficiencies',
            field=models.ManyToManyField(blank=True, related_name='character_classes_with_proficiency', to='main.proficiency'),
        ),
        migrations.AddField(
            model_name='characterclass',
            name='saving_throws',
            field=models.ManyToManyField(blank=True, related_name='saving_throws', to='main.abilityscore'),
        ),
        migrations.AddField(
            model_name='characterclass',
            name='starting_equipment',
            field=models.ManyToManyField(blank=True, through='main.StartingEquipment', to='main.equipment'),
        ),
        migrations.AddField(
            model_name='abilityscore',
            name='skills',
            field=models.ManyToManyField(blank=True, to='main.skill'),
        ),
    ]
