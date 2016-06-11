import requests
import redis
import json
from brewmaster.settings import AVERY_API_ROOT, REDIS_HOST


def avery(url):
    if AVERY_API_ROOT in url:
        return requests.get(url).json()
    else:
        return requests.get(AVERY_API_ROOT + url).json()


def get_beers(refresh_cache=False):
    r = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)
    if refresh_cache:
        beers = avery('beers')['beers']
        result = json.dumps([avery(beer['url']) for beer in beers])
        r.set('beers', result)
    return json.loads(str(r.get('beers')))