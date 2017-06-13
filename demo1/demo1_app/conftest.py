

import pytest

from demo1_app.models import Foobar

SESSION_FIXTURE = "session_fixture"

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        Foobar.objects.create(name=SESSION_FIXTURE)

