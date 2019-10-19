from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views import View


def index(request):
    return HttpResponse("OK")
class register(View):
    def get(self):
        return HttpResponse("ok")