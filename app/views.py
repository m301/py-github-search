import datetime
import json
import requests
from django.shortcuts import render, HttpResponse
from pymongo import MongoClient

db = MongoClient()['test']
collection = db['store']


# Create your views here.

def index(request):
    return HttpResponse('Hello World!')


def search(request):
    # TODO : to handle timeout exception
    # Length validation
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', '')
    order = request.GET.get('order', 'desc')
    endpoint = 'search/users?q=%s' % (query)
    if bool(sort):
        endpoint = endpoint + ('&sort=%s&order=%s' % (sort, order))
    req = requests.get('https://api.github.com/'+endpoint)
    data = json.loads(req.content)

    # insert hits to database. if request is successful
    db['hits'].insert({'time': datetime.datetime.utcnow(),'endpoint':endpoint})

    for item in data.get("items", []):
        record = {}
        item['_id'] = item.get('login')
        item['_update_time'] = datetime.datetime.utcnow()
        record['$set'] = item
        collection.update({'_id': item.get('_id')}, record, upsert=True)

    return render(request, 'app/search.html', {'data': data.get("items", [])})


def profile(request):
    pass
    # return HttpResponse(parsedData)
