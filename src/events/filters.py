import django_filters
from events.models import Event


class EventFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    location = django_filters.CharFilter(lookup_expr="icontains")
    date_from = django_filters.DateTimeFilter(field_name="date", lookup_expr="gte")
    date_to = django_filters.DateTimeFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Event
        fields = ["title", "location", "date_from", "date_to"]
