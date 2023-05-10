from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from company.filters import EmployeeFilter, ReservationFilter, RoomFilter

from company.models import Employee, Reservation, Room
from company.serializers import (
    AttendeeAddSerializer,
    EmployeeSerializer,
    ReservationSerializer,
    RoomSerializer,
)


class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EmployeeFilter


class RoomViewSet(ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RoomFilter


class ReservationViewSet(ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReservationFilter

    @action(detail=True, methods=["PUT"], serializer_class=AttendeeAddSerializer)
    def add_attendee(self, request: Request, pk: int | None = None):
        reservation = self.get_object()
        serializer = self.get_serializer(
            reservation,
            data=request.data,
            partial=True,
            context={"reservation": reservation},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
