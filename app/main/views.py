from django.contrib.sites import requests
from django.shortcuts import render
import requests


def index(request):

    #

    url = "https://www.dnd5eapi.co/api/proficiencies/battleaxes"



    #
    headers = {
        'Accept': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    response_data = response.json()

    context =  {
        "response_data": response_data,
        "title": "Создание персонажа",
    }

    return render (request, 'index.html',context)