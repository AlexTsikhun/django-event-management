from common.containers import DjangoUnitOfWork
from events.repositories import EventRegistrationRepository, EventRepository


class EventUnitOfWork(DjangoUnitOfWork):
    def __init__(self):
        self.events = EventRepository()
        self.event_managers = EventRegistrationRepository()
