import pytest

from django.test import TestCase
from django.urls import reverse
from model_bakery.baker import make
from rest_framework import status

from company.models import Employee, Room


@pytest.mark.django_db
class TestEmployee:
    def test_employee_list(self, client):
        make(Employee, _quantity=2)

        response = client.get(reverse("employees-list"))

        assert response.status_code, status.HTTP_200_OK
        assert len(response.data) == 2

    def test_employee_get(self, client, employee):
        response = client.get(reverse("employees-detail", args=[employee.id]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == employee.first_name
        assert response.data["last_name"] == employee.last_name
        assert response.data["email"] == employee.email
        assert response.data["position"] == employee.position
        assert response.data["experience"] == employee.experience

    def test_employee_post(self, client, employee):
        payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@domain.com",
            "position": "manager",
            "experience": 10,
        }

        response = client.post(reverse("employees-list"), payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Employee.objects.count() == 2

        employee = Employee.objects.filter(first_name=payload["first_name"]).first()
        assert employee.first_name == payload["first_name"]
        assert employee.last_name == payload["last_name"]
        assert employee.email == payload["email"]
        assert employee.position == payload["position"]
        assert employee.experience == payload["experience"]

    def test_employee_put(self, client, employee):
        payload = {
            "first_name": "Johnny",
            "last_name": "Doe",
            "email": "johnny.doe@example.com",
            "position": "senior_developer",
            "experience": 7,
        }

        response = client.put(
            reverse("employees-detail", args=[employee.id]),
            payload,
            content_type="application/json",
        )

        assert response.status_code, status.HTTP_200_OK
        employee.refresh_from_db()
        assert employee.first_name == payload["first_name"]
        assert employee.last_name == payload["last_name"]
        assert employee.email == payload["email"]
        assert employee.position == payload["position"]
        assert employee.experience == payload["experience"]

    def test_employee_patch(self, client, employee):
        payload = {"position": "designer", "experience": 10}

        response = client.patch(
            reverse("employees-detail", args=[employee.id]),
            payload,
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_200_OK
        employee.refresh_from_db()
        assert employee.position == payload["position"]
        assert employee.experience == payload["experience"]

    def test_employee_delete(self, client, employee):
        response = client.delete(reverse("employees-detail", args=[employee.id]))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Employee.objects.count() == 0


@pytest.mark.django_db
class TestRoom:
    def test_room_list(self, client, room):
        make(Room, _quantity=2)

        response = client.get(reverse("rooms-list"))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_room_get(self, client, room):
        response = client.get(reverse("rooms-detail", args=[room.id]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == room.name
        assert response.data["capacity"] == room.capacity

    def test_employee_post(self, client, room):
        payload = {"name": "Meeting room 2", "capacity": 25}

        response = client.post(reverse("rooms-list"), payload)

        assert response.status_code == status.HTTP_201_CREATED
        room = Room.objects.filter(name=payload["name"]).first()
        assert room.name == payload["name"]
        assert room.capacity == payload["capacity"]

    def test_room_put(self, client, room):
        payload = {"name": "Meeting room 0", "capacity": 100}

        response = client.put(
            reverse("rooms-detail", args=[room.id]),
            payload,
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_200_OK
        room.refresh_from_db()
        assert room.name == payload["name"]
        assert room.capacity == payload["capacity"]

    def test_room_patch(self, client, room):
        payload = {
            "capacity": 100,
        }

        response = client.patch(
            reverse("rooms-detail", args=[room.id]),
            payload,
            content_type="application/json",
        )

        assert response.status_code, status.HTTP_200_OK
        room.refresh_from_db()
        assert room.capacity == payload["capacity"]

    def test_room_delete(self, client, room):
        response = client.delete(reverse("rooms-detail", args=[room.id]))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Room.objects.count() == 0
