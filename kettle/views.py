from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .utils import get_beers
from django.shortcuts import render
from .scripts.trainClassifier import LRBeerClassifier
import simplejson as json

# Create your views here.

def index(request):
    beers = get_beers()
    return render(request, 'kettle/index.html', {'beers': beers})

def beer_list(request):
    beers = get_beers()
    return JsonResponse({"result": beers})

def crunch(request):
    print(request.body)
    received_json_data = json.loads(request.body)
    like_ids = received_json_data['like_ids']
    dislike_ids = received_json_data['dislike_ids']
    classifier = LRBeerClassifier()
    classifier.train(like_ids, dislike_ids)
    other_beers = [b for b in get_beers() if b['id'] not in like_ids + dislike_ids]
    results = [(beer['id'], classifier.classify(beer['id'])) for beer in other_beers]
    return JsonResponse({"result": sorted(results, key=lambda x: x[1], reverse=True)})
