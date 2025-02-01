from django.contrib.sites import requests
from django.shortcuts import render
import requests

# Create your views here.

# def index(request):
#
#     context = {
#         'title' : "Создание персонажа"
#     }
#
#     return render(request, "index.html", context)

def index(request):


    # name = request.GET['name']
    url = "https://www.dnd5eapi.co/api/races/dwarf"
    payload = {}
    headers = {
        'Accept': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)    # response = requests.get(url)
    response_data = response.text
    # meals = data['meals']    # for i in meals:
    #     meal_data = Meal(
    #         name = i['strMeal'],
    #         category = i['strCategory'],
    #         instructions = i['strInstructions'],
    #         region = i['strArea'],
    #         slug = i['idMeal'],
    #         image_url = i['strMealThumb']
    #     )
    #     meal_data.save()
    #     all_meals = Meal.objects.all().order_by('-id')
    context =  {
        "response_data": response_data,
        "title": "Создание персонажа"
    }

    return render (request, 'index.html',context)