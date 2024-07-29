from django.http import HttpResponse

def hello_django(request):
    return HttpResponse("Hello, Django")