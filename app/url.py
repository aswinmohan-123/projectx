from django.conf.urls import url
from app.views import login
from app.rendering import home

urlpatterns = [
    url(r'^login', login.as_view()),
    url(r'^home', home)
]