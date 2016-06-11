import requests
import redis
import simplejson as json
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
        result = []
        for beer in beers:
            print(beer['name'])
            result.append(avery(beer['url'])['beer'])
        r.set('beers', json.dumps(result))
    return json.loads(r.get('beers'))