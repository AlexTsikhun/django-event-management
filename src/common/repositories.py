from common.interfaces import AbstractRepository


class DjangoRepository(AbstractRepository):
    model_class = None

    def list(self, **filters):
        return self.model_class.objects.filter(**filters)

    def create(self, data):
        return self.model_class.objects.create(**data)

    def update(self, reference, data):
        return self.model_class.objects.filter(id=reference).update(**data)

    def retrieve(self, reference):
        return self.model_class.objects.filter(id=reference).first()

    def delete(self, reference):
        return self.model_class.objects.filter(id=reference).delete()
