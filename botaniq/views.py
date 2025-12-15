from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    """Home page for BotanIQ"""
    return HttpResponse("Welcome to BotanIQ - Discover the Botanical Intelligence of Traditional Medicine!")
