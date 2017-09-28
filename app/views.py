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
    req = requests.get('https://api.github.com/' + endpoint)
    data = json.loads(req.content)

    # insert hits to database. if request is successful
    db['hits'].insert({'time': datetime.datetime.utcnow(), 'endpoint': endpoint})

    for item in data.get("items", []):
        record = {}
        item['_id'] = item.get('login')
        item['_update_time'] = datetime.datetime.utcnow()
        record['$set'] = item
        collection.update({'_id': item.get('_id')}, record, upsert=True)

    return render(request, 'app/search.html', {'data': data.get("items", [])})


def get_stat(collection,field):
    hits_by_days = [
        {'$group': {'_id': {
            'year': {'$year': field},
            'month': {'$month': field},
            'day': {'$dayOfMonth': field}
        },
            'count': {'$sum': 1}
        }
        }
    ]

    hits_by_week = [
        {'$group': {'_id': {
            'week': {'$week': field},
        },
            'count': {'$sum': 1}
        }
        }
    ]

    hits_by_months = [
        {'$group': {'_id': {
            'month': {'$month': field},
        },
            'count': {'$sum': 1}
        }
        }
    ]

    response = {'days':list(collection.aggregate(hits_by_days)),'weeks':list(collection.aggregate(hits_by_week)),'months':list(collection.aggregate(hits_by_months))}
    return response 


def get_system_stat(request):
    response = {'hits':get_stat(db['hits'],"$time"),
                'records':get_stat(collection,"$_update_time")}
    print(response)
    # create a html to render this json
    return render(request,"app/stats.html",response)

def get_all(request):
    users = list(collection.find())
    return render(request, 'app/search.html', {'data': users})

def profile(request):
    pass
    # return HttpResponse(parsedData)
