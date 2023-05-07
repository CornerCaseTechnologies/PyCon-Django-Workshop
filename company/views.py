from rest_framework.viewsets import ModelViewSet

from company.models import Employee, Reservation, Room
from company.serializers import EmployeeSerializer, ReservationSerializer, RoomSerializer


class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class RoomViewSet(ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()


class ReservationViewSet(ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
