from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Class Based Views 
class Github_view(View):

    def get(self, request):
        return HttpResponse("Hello, APIs")
