from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def editor(request):
    return render(request, 'editor/editor.html')