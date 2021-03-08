from django.shortcuts import render, redirect
from .models import *
import requests
from .forms import *

# Create your views here.

def home(request):

    #Get API url
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID=565800264887cf0b6a19b3ab7c6b7a85'

    cities = City.objects.all()
    form = CityForm()

    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            count = City.objects.filter(name=new_city).count()

        if count == 0:
            r = requests.get(url.format(new_city)).json()
            if r['cod'] == 200:
                form.save()
                message = 'City has been added!'
                message_class = 'is-success'
            else:
                message = 'Could not find that city!'
                message_class = 'is-danger'
        else:
            message = 'That city is already logged!'
            message_class = 'is-danger'


    weather_data = []
    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'name': city,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form':form, 'message':message, 'message_class':message_class}

    return render(request, 'home.html', context)


def delete(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')

#delte cities (button)
