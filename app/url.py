from django.conf.urls import url
from app.views import login

urlpatterns = [
    url(r'^login', login.as_view()),
]