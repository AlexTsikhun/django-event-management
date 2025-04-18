from collections.abc import Sequence
from django.core.mail import EmailMessage


def send_email(
    subject: str,
    content,
    from_email: str,
    to_email: str | Sequence[str],
):
    message = EmailMessage(
        subject=subject,
        body=content,
        from_email=from_email,
        to=[to_email] if isinstance(to_email, str) else to_email,
    )
    message.content_subtype = "html"
    message.send()
