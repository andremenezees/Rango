from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def rango(request):
    return HttpResponse('<html><body>Rango says hey there partner!</body></html>', content_type='text/html')


def about(request):
    return HttpResponse('<html><body>Rango says here is the about page.</body></html>', content_type='text/html')


def index(request):
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}

    return render(request, 'rango/index.html', context=context_dict)
