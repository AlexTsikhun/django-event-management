from collections.abc import Sequence

from events.tasks import send_email


def send_notification(
    from_email: str, to_email: str | Sequence[str], subject: str, content: dict
):
    send_email.delay(from_email, to_email, subject, content)
