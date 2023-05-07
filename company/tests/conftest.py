import pytest
from company.models import Employee, Room
from model_bakery.baker import make

@pytest.fixture
def employee():
    return make(
        Employee,
        first_name='John',
        last_name='Doe',
        email='john.doe@domain.com',
        position='Software Developer',
        experience=2
    )

@pytest.fixture
def room():
    return make(Room, name='Meeting Room 1', capacity=30)
