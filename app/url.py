from django.conf.urls import include,url
from app.views import login

urlpatterns = [
    url('^/login', login.as_view()),
]