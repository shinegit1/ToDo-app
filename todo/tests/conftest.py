import pytest
import os
from django.core.management import call_command
from todo_project.settings import BASE_DIR


file_path = os.path.join(BASE_DIR, 'relative_path')

@pytest.fixture(scope='function')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        test_db_file_path = os.path.join(BASE_DIR, 'todo/tests/test_db.json')
        call_command('loaddata', test_db_file_path)
