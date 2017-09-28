
from django.shortcuts import render, HttpResponse
import requests
import json

# Create your views here.

def index(request):
    return HttpResponse('Hello World!')

def search(request):
    # Length validation
    query = request.GET.get('q', '')

    req = requests.get('https://api.github.com/search/users?q=%s'%(query))
    data  = json.loads(req.content)
    # print data
    return render(request, 'app/search.html', {'data':data.get("items",[])})

def profile(request):
    pass
    # return HttpResponse(parsedData)