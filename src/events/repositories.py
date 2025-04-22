from common.repositories import DjangoRepository
from events.models import Event, EventRegistration


class EventRepository(DjangoRepository):
    model_class = Event


class EventRegistrationRepository(DjangoRepository):
    model_class = EventRegistration
