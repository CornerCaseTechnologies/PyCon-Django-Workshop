from rest_framework.viewsets import ModelViewSet

from company.models import Employee, Room
from company.serializers import EmployeeSerializer, RoomSerializer


class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class RoomViewSet(ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
