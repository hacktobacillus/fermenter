import requests
import simplejson as json
from brewmaster.settings import AVERY_API_ROOT
from kettle.models import Cache


def avery(url):
    if AVERY_API_ROOT in url:
        return requests.get(url).json()
    else:
        return requests.get(AVERY_API_ROOT + url).json()


def get_beers(refresh_cache=False):
    if refresh_cache:
        beers = avery('beers')['beers']
        result = []
        for beer in beers:
            print(beer['name'])
            result.append(avery(beer['url'])['beer'])
        Cache(key='beer_list', value=json.dumps(result)).save()
    return json.loads(Cache.objects.get(key='beer_list').value)