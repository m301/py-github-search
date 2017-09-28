import json
import requests
from django.shortcuts import render, HttpResponse
from pymongo import MongoClient
import datetime
collection = MongoClient()['test']['store']


# Create your views here.

def index(request):
    return HttpResponse('Hello World!')


def search(request):
    # Length validation
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', '')
    order = request.GET.get('order', 'desc')
    url = 'https://api.github.com/search/users?q=%s' % (query)
    if bool(sort):
        url = url + ('&sort=%s&order=%s' % (sort, order))
    req = requests.get(url)
    data = json.loads(req.content)

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
