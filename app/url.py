from django.conf.urls import url
from app.views import Login, Register, Details, Inbox, Peoples, Send
from app.rendering import home

urlpatterns = [
    url(r'^login', Login.as_view()),
    url(r'^register', Register.as_view()),
    url(r'^details', Details.as_view()),
    url(r'^inbox', Inbox.as_view()),
    url(r'^peoples', Peoples.as_view()),
    url(r'^send', Send.as_view()),
    url(r'^home', home)
]