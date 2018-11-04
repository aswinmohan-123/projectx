from django.shortcuts import render
from django.template import loader

class home():
    def __init__(self, request):
        template = loader.get_template('base_page.html')
        return template.render(request)