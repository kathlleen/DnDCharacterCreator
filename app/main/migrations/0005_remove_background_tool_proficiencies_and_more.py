# Generated by Django 4.2.14 on 2025-02-13 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_background_tool_proficiencies_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='background',
            name='tool_proficiencies',
        ),
        migrations.AddField(
            model_name='background',
            name='tool_proficiencies',
            field=models.TextField(blank=True, null=True),
        ),
    ]
