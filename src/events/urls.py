from django.urls import path, include
from rest_framework.routers import DefaultRouter

from events.views import EventViewSet


app_name = "events"

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="events")
# router.register(r'registrations', EventRegistrationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
