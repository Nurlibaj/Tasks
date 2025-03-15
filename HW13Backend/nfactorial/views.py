from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Hello, nfactorial school!.")
def add(request, first, second):
    c = int(first) + int(second)
    return HttpResponse(f"Result: {c}")
def transform(request, text):
    result = text.upper()
    return HttpResponse(result)