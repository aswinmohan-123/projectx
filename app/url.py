from django.conf.urls import url
from app.views import Login, Register
from app.rendering import home

urlpatterns = [
    url(r'^login', Login.as_view()),
    url(r'^register', Register.as_view()),
    url(r'^home', home)
]