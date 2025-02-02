from django.contrib.sites import requests
from django.shortcuts import render
import requests

from main.models import Race


# Create your views here.

# def index(request):
#
#     context = {
#         'title' : "Создание персонажа"
#     }
#
#     return render(request, "index.html", context)

def index(request):


    # values = ['dragonborn', 'dwarf', 'elf', 'gnome', 'half-elf', 'half-orc', 'halfling', 'human', 'tiefling']
    # base_url = "https://www.dnd5eapi.co/api/races/"
    # payload = {}
    # headers = {
    #     'Accept': 'application/json'
    # }
    # for value in values:
    #     url = base_url + value
    #     response = requests.request("GET", url, headers=headers, data=payload)    # response = requests.get(url)
    #     response_data = response.json()
    #
    #     all_traits = response_data['traits']
    #     traits = ''
    #     for i in all_traits:
    #         traits += i['name']
    #         traits += ", "
    #     # print(f'{value} traits: {traits}')
    #
    #     all_languages = response_data['languages']
    #     languages = ''
    #     for i in all_languages:
    #         languages += i['name']
    #         languages += ", "
    #
    #     race_data = Race(
    #         index = response_data['index'],
    #         name = response_data['name'],
    #         speed = response_data['speed'],
    #         age = response_data['age'],
    #         alignment = response_data['alignment'],
    #         size = response_data['size'],
    #         size_description = response_data['size_description'],
    #         language_desc = response_data['language_desc'],
    #         languages = languages,
    #         traits = traits,
    #     )
    #     race_data.save()

    all_races = Race.objects.all().order_by('-id')

    context =  {
        # "response_data": response_data,
        "title": "Создание персонажа",
        'races':all_races
    }

    return render (request, 'index.html',context)