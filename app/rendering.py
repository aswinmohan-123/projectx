from django.shortcuts import render
from django.middleware.csrf import get_token


def home(request):
    token = get_token(request)
    return render(request, 'base_page.html', context={"csrf_token": token})

