from django.urls import path

from events.views import hello_world

app_name = "events"


urlpatterns = [
    path("", hello_world, name="hello_world"),
]
