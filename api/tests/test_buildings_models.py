import pytest

from django.utils import timezone
from buildings.models import Building


@pytest.fixture
def min_building_fixture():
	# required fields for Building object
	return {
		'risk_category': 'risk 1',
		'county': 'Cluj',
		'post_code': '400004',
		'locality': 'Cluj-Napoca',
	}


@pytest.fixture
def full_building_fixture(min_building_fixture):

	extra_fields = {
		'registration_number' : 1234,
		'examination_year' : 1234,
		'certified_expert' : '1234',
		'observations' : '1234',
		'lat' : 12.34,
		'lng' : 12.34,
		'address' : '1234 1234 1234',
		'year_built' : 1234,
		'height_regime' : '1234',
		'apartment_count' : 1234,
		'surface' : 1234,
		'cadastre_number' : 1234,
		'land_registry_number' : '1234',
		'administration_update' : '2000-01-21',
		'admin_update' : '2001-02-20',
		'status' : 1
	}
	extra_fields.update(**min_building_fixture)

	return extra_fields

@pytest.mark.django_db
def test_minimum_building_create(min_building_fixture):
	# Check that a building is created with just the minimum required fields
	Building.objects.create(**min_building_fixture)
	assert Building.objects.count() == 1

	# Validate default attributes
	building = Building.objects.first()
	assert building.status == 0

	# Allow for a 2 seconds range on created field
	now = timezone.now()
	delta = timezone.timedelta(seconds=2)
	assert now - delta < building.created_on < now


@pytest.mark.django_db
def test_full_building_create(full_building_fixture):
	Building.objects.create(**full_building_fixture)
	assert Building.objects.count() == 1

	building = Building.objects.first()
	assert str(building) == '1234 1234 1234'
