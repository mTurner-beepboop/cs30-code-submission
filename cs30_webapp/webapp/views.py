from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request,'webapp/home.html')

def dbview(request):
    return render(request,'webapp/dbview.html')
