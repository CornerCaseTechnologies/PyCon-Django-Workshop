from datetime import datetime

from django_filters import (
    FilterSet,
    NumberFilter,
    BooleanFilter,
    CharFilter,
    ChoiceFilter,
)
from django.db.models import Q
from django.db.models.query import QuerySet
from company import Positions

from company.models import Employee, Reservation, Room


class RoomFilter(FilterSet):
    min_capacity = NumberFilter(field_name="capacity", lookup_expr="gte")
    is_reserved = BooleanFilter(method="filter_reserved", label="Is Reserved")

    class Meta:
        model = Room
        fields = ["min_capacity", "is_reserved"]

    def filter_reserved(
        self, queryset: QuerySet[Room], name: str, value: bool | None
    ) -> QuerySet[Room]:
        now = datetime.now()
        reserved_rooms = queryset.filter(
            reservations__reserved_from__lte=now, reservations__reserved_to__gt=now
        )
        if value:
            return reserved_rooms
        elif value == None:
            return queryset
        elif not value:
            return queryset.exclude(pk__in=reserved_rooms.values_list("pk", flat=True))


class EmployeeFilter(FilterSet):
    name = CharFilter(method="filter_name", label="Name")
    max_experience = NumberFilter(field_name="experience", lookup_expr="lte")
    assumed_position = ChoiceFilter(choices=Positions)

    class Meta:
        model = Employee
        fields = ["name", "max_experience", "assumed_position"]

    def filter_name(
        self, queryset: QuerySet[Employee], name: str, value: str
    ) -> QuerySet[Employee]:
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value)
        )


class ReservationFilter(FilterSet):
    room_id = NumberFilter(field_name="room__id")

    class Meta:
        model = Reservation
        fields = ["room_id"]
