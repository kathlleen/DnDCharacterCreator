from django.contrib.sites import requests
from django.shortcuts import render
import requests


def index(request):
    #
    #
    # url = "https://www.dnd5eapi.co/api/classes/bard"
    #
    # headers = {
    #     'Accept': 'application/json'
    # }
    # response = requests.request("GET", url, headers=headers)
    # response_data = response.json()
    #
    # hit_die = response_data['hit_die']
    #
    #
    # choose = response_data['proficiency_choices'][0]['choose']
    # proficiencies = []
    # proficiencies_data = response_data['proficiency_choices'][0]['from']['options']
    #
    # for item in proficiencies_data:
    #     proficiencies.append(item['item']['name'][7:])
    # all_proficiencies = ', '.join(proficiencies)
    #
    #
    context =  {
        # "response_data": response_data,
        "title": "Создание персонажа",
        # 'data':all_proficiencies,
        # 'choose':choose
    }

    return render (request, 'index.html',context)