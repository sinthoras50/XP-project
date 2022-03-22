import json
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from matplotlib.font_manager import json_load 

# Create your views here.

def home(request):

    return render(request, 'home/home.html')

@csrf_exempt
def upload(request):

    if request.method == 'POST':


        print(request.FILES['file'].file.getvalue().decode("utf-8"))

        ret = {
            "bu" : 1,
            "mu" : 2,
            "lu" : ["a", "b", "c"]
        }

        return HttpResponse(json.dumps(ret))
