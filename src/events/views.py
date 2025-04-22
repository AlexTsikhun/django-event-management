from rest_framework import viewsets, permissions, status
from events.containers import EventUnitOfWork
from events.permissions import IsOrganizerOrReadOnly
from events.serializer import EventSerializer, EventRegistrationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from events.filters import EventFilter


from events.use_cases.events import EventUseCase, EventRegistrationUseCase


class EventViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def get_use_case(self):
        return EventUseCase(EventUnitOfWork())

    def list(self, request):
        use_case = self.get_use_case()
        filters = self.filterset_class(
            request.query_params, queryset=use_case.list_events()
        ).qs
        serializer = EventSerializer(filters, many=True)
        return Response(serializer.data)

    def create(self, request):
        use_case = self.get_use_case()
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event = use_case.create_event(
                organizer=request.user, data=serializer.validated_data
            )
            return Response(EventSerializer(event).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        use_case = self.get_use_case()
        event = use_case.retrieve_event(pk)
        if not event:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(EventSerializer(event).data)

    def update(self, request, pk=None):
        use_case = self.get_use_case()
        serializer = EventSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            event = use_case.update_event(pk, serializer.validated_data)
            if not event:
                return Response(
                    {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
                )
            return Response(EventSerializer(event).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        use_case = self.get_use_case()
        use_case.delete_event(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def register(self, request, pk=None):
        use_case = EventRegistrationUseCase(EventUnitOfWork())
        try:
            registration = use_case.register_user(user=request.user, event_id=pk)
            return Response(
                EventRegistrationSerializer(registration).data,
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EventRegistrationViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_use_case(self):
        return EventRegistrationUseCase(EventUnitOfWork())

    def list(self, request):
        use_case = self.get_use_case()
        registrations = use_case.list_user_registrations(user=request.user)
        serializer = EventRegistrationSerializer(registrations, many=True)
        return Response(serializer.data)
