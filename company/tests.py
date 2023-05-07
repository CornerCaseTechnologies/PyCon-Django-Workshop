import datetime

import pytest
from django.test import TestCase
from django.urls import reverse
from model_bakery.baker import make
from rest_framework import status

from company.models import Employee, Room


class TestEmployee:
    def setup_method(self):
        self.employee = make(
            Employee,
            first_name='John',
            last_name='Doe',
            email='john.doe@gmail.com',
            position='Software Developer',
            experience=2,
            date_of_birth=datetime.date(1998, 1, 1)
        )

        self.employee_list_url = reverse('employees-list')
        self.employee_detail_url = reverse('employees-detail', args=[self.employee.id])

    @pytest.mark.django_db
    def test_employee_list(self, client):
        make(Employee, _quantity=2)

        response = client.get(self.employee_list_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    @pytest.mark.django_db
    def test_employee_get(self, client):
        response = client.get(self.employee_detail_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == self.employee.first_name
        assert response.data['last_name'] == self.employee.last_name
        assert response.data['email'] == self.employee.email
        assert response.data['experience'] == self.employee.experience

    @pytest.mark.django_db
    def test_employee_post(self, client):
        payload = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@gmail.com',
            'position': 'CEO',
            'experience': 10,
            'date_of_birth': datetime.date(1998, 1, 1)
        }

        response = client.post(self.employee_list_url, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Employee.objects.count() == 2
        employee = Employee.objects.filter(first_name=payload['first_name']).first()
        assert employee.first_name == payload['first_name']
        assert employee.last_name == payload['last_name']
        assert employee.email == payload['email']
        assert employee.position == payload['position']
        assert employee.experience == payload['experience']

    @pytest.mark.django_db
    def test_employee_put(self, client):
        payload = {
            'first_name': 'Johnny',
            'last_name': 'Doe',
            'email': 'johnny.doe@gmail.com',
            'position': 'Senior Developer',
            'experience': 7,
            'date_of_birth': datetime.date(1998, 1, 1)
        }

        response = client.put(self.employee_detail_url, payload, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        self.employee.refresh_from_db()
        assert self.employee.first_name == payload['first_name']
        assert self.employee.last_name == payload['last_name']
        assert self.employee.email == payload['email']
        assert self.employee.position == payload['position']
        assert self.employee.experience == payload['experience']
        assert self.employee.date_of_birth == payload['date_of_birth']

    @pytest.mark.django_db
    def test_employee_patch(self, client):
        payload = {
            'experience': 10
        }

        response = client.patch(self.employee_detail_url, payload, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        self.employee.refresh_from_db()
        assert self.employee.experience == payload['experience']

    @pytest.mark.django_db
    def test_employee_delete(self, client):
        response = client.delete(self.employee_detail_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Employee.objects.count() == 0


class RoomTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.room = make(Room, name='Meeting Room 1', capacity=30)

        self.room_list_url = reverse('rooms-list')
        self.room_detail_url = reverse('rooms-detail', args=[self.room.id])

    def test_room_list(self):
        make(Room, _quantity=2)

        response = self.client.get(self.room_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_room_get(self):
        response = self.client.get(self.room_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.room.name)
        self.assertEqual(response.data['capacity'], self.room.capacity)

    def test_employee_post(self):
        payload = {
            'name': 'Meeting room 2',
            'capacity': 25
        }

        response = self.client.post(self.room_list_url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        room = Room.objects.filter(name=payload['name']).first()
        self.assertEqual(room.name, payload['name'])
        self.assertEqual(room.capacity, payload['capacity'])

    def test_room_put(self):
        payload = {
            'name': 'Meeting room 0',
            'capacity': 100
        }

        response = self.client.put(self.room_detail_url, payload, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.room.refresh_from_db()
        self.assertEqual(self.room.name, payload['name'])
        self.assertEqual(self.room.capacity, payload['capacity'])

    def test_room_patch(self):
        payload = {
            'capacity': 100,
        }

        response = self.client.patch(self.room_detail_url, payload, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.room.refresh_from_db()
        self.assertEqual(self.room.capacity, payload['capacity'])

    def test_room_delete(self):
        response = self.client.delete(self.room_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Room.objects.count(), 0)
