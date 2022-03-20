from distutils.command.upload import upload
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.

def welcome(request):

    if request.method == 'POST':
        uploaded_file = request.FILES['file']

        print(uploaded_file.name)
        print(uploaded_file.read())

    return render(request, 'welcome/welcome.html')
