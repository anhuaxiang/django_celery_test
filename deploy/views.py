from django.shortcuts import render
from .tasks import add


# Create your views here.
def post(request):
    result = add.delay(2, 3)
