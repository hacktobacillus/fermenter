from django.shortcuts import render
from django.http import HttpResponse
from .utils import get_beers
from django.shortcuts import render
from .scripts.trainClassifier import LRBeerClassifier
import json

# Create your views here.

def index(request):
    beers = get_beers()
    return render(request, 'kettle/index.html', {'beers': beers})

def beer_list(request):
    beers = get_beers()
    return render(request, 'kettle/beer_list.html', {'beers': beers})

def crunch(request):
    like_ids = []
    dislike_ids = []
    classifier = LRBeerClassifier()
    classifier.train(like_ids, dislike_ids)
    results = sorted([(beer['id'], classifier.classify(beer['id'])) for beer in get_beers()], lambda x: x[1], reversed=True)
    return json.dumps(results)

