from common.interfaces import AbstractUnitOfWork
from events.notifiers import send_notification

from django.template.loader import render_to_string

from event_management import settings


class EventUseCase:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def create_event(self, organizer, data):
        with self.uow:
            event = self.uow.events.create({**data, "organizer": organizer})
            return event

    def list_events(self, **filters):
        with self.uow:
            return self.uow.events.list(**filters)

    def retrieve_event(self, event_id):
        with self.uow:
            return self.uow.events.retrieve(event_id)

    def update_event(self, event_id, data):
        with self.uow:
            self.uow.events.update(event_id, data)
            return self.uow.events.retrieve(event_id)

    def delete_event(self, event_id):
        with self.uow:
            self.uow.events.delete(event_id)


class EventRegistrationUseCase:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def register_user(self, user, event_id):
        with self.uow:
            event = self.uow.events.retrieve(event_id)
            if not event:
                raise ValueError("Event does not exist")

            if self.uow.event_registrations.list(event=event, user=user):
                raise ValueError("User already registered for this event")

            registration = self.uow.event_registrations.create(
                {"event": event, "user": user}
            )

            subject = f"Registration Confirmation for {event.title}"
            html_message = render_to_string(
                "email/registration_confirmation.html",
                {"user": user, "event": event},
            )
            send_notification(
                from_email=settings.EMAIL_HOST_USER,
                to_email=[user.email],
                subject=subject,
                content=html_message,
            )

            return registration

    def list_user_registrations(self, user):
        with self.uow:
            return self.uow.event_registrations.list(user=user)
