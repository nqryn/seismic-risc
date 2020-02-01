import pytest
import os
import tempfile
import shutil

from django.core.files import File
from django.conf import settings

from buildings.models import CsvFile

@pytest.fixture
def min_csv_fixture(settings):
	# setup
	settings.MEDIA_ROOT = tempfile.mkdtemp()
	print(settings.MEDIA_ROOT)
	
	filename = 'tmp.csv'
	filepath = os.path.join(settings.MEDIA_ROOT, filename)

	with open(filepath, 'w') as csv_in:
		csv_in.writelines([
			'a, b, c, d, e, f\n',
			'1, 2, 3, 4, 5, 6\n',
			'C, S, V, I, N'
		])

	f = open(filepath)
	yield {
		'name': filename,
		'file': File(f)
	}

	# tear down
	f.close()
	shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)


@pytest.mark.django_db
def test_minimum_csv_create(min_csv_fixture):
	# Check that a CsvFile is created with just the minimum required fields
	CsvFile.objects.create(**min_csv_fixture)
	assert CsvFile.objects.count() == 1

	# Validate default attributes
	csv_file = CsvFile.objects.first()
	assert csv_file.status == CsvFile.NOT_TRIED
	assert str(csv_file) == csv_file.name

@pytest.mark.django_db
def test_edit_status(min_csv_fixture):
	# Try to edit status field, it should be possible from code
	min_csv_fixture['status'] = CsvFile.SUCCESS
	CsvFile.objects.create(**min_csv_fixture)
	assert CsvFile.objects.count() == 1

	# Validate default attributes
	csv_file = CsvFile.objects.first()
	assert csv_file.status == CsvFile.SUCCESS

	csv_file.status = CsvFile.UNSUCCESS
	csv_file.save()
	assert csv_file.status == CsvFile.UNSUCCESS


@pytest.mark.django_db
def test_delete_csv(min_csv_fixture):
	# Deleting the model instance should NOT delete the file as well
	CsvFile.objects.create(**min_csv_fixture)

	csv_file = CsvFile.objects.filter(name=min_csv_fixture['name']).first()
	assert csv_file is not None

	filepath = csv_file.file.path
	assert os.path.exists(filepath)
	csv_file.delete()
	assert os.path.exists(filepath)
	
