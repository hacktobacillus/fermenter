from django.shortcuts import render
from django.http import HttpResponse
from kettle.utils import get_beers
from django.shortcuts import render

# Create your views here.

def index(request):
    beers = get_beers()
    return render(request, 'kettle/index.html', {'beers': beers})

def beer_list(request):
    beers = get_beers()
    return render(request, 'kettle/beer_list.html', {'beers': beers})
