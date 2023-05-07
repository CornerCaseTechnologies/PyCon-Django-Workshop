from django.urls import path, include
from rest_framework.routers import DefaultRouter

from company.views import EmployeeViewSet, ReservationViewSet, RoomViewSet

router = DefaultRouter()
router.register("employees", EmployeeViewSet, basename="employees")
router.register("rooms", RoomViewSet, basename="rooms")
router.register("reservations", ReservationViewSet, basename="reservations")

urlpatterns = [
    path("", include(router.urls))
]
