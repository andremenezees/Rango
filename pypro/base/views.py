from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def rango(request):
    return HttpResponse('<html><body>Rango says hey there partner!</body></html>', content_type='text/html')


def about(request):
    return render(request, 'rango/about.html')


def index(request):
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}

    return render(request, 'rango/index.html', context=context_dict)
