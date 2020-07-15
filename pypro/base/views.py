from django.http import HttpResponse


def rango(request):
    return HttpResponse('<html><body>Rango says hey there partner!</body></html>', content_type='text/html')
