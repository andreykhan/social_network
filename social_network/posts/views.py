from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('main page')


def posts(request, slug):
    return HttpResponse('posts page')
