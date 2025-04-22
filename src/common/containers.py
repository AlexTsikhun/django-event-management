from django.db import transaction

from common.interfaces import AbstractUnitOfWork


class DjangoUnitOfWork(AbstractUnitOfWork):
    def __enter__(self):
        self.atomic = transaction.atomic()
        self.atomic.__enter__()

    def __exit__(self, *args, **kwargs):
        self.atomic.__exit__(*args, **kwargs)
