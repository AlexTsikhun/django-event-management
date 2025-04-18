from collections.abc import Sequence

from events import services
from celery import shared_task


@shared_task
def send_email(
    from_email: str,
    to_email: str | Sequence[str],
    subject: str,
    content: str,
):
    services.send_email(subject, content, from_email, to_email)
