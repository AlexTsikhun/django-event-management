# Create your views here.
from rest_framework import viewsets, permissions, status
from events.permissions import IsOrganizerOrReadOnly
from events.serializer import EventSerializer, EventRegistrationSerializer
from events.models import Event, EventRegistration
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from events.filters import EventFilter


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def register(self, request, pk=None):
        event = self.get_object()
        if EventRegistration.objects.filter(event=event, user=request.user).exists():
            return Response(
                {"error": "Already registered"}, status=status.HTTP_400_BAD_REQUEST
            )

        registration = EventRegistration.objects.create(event=event, user=request.user)

        return Response(
            EventRegistrationSerializer(registration).data,
            status=status.HTTP_201_CREATED,
        )


class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
