import pytest

from demo2_app.conftest import SESSION_FIXTURE
from demo2_app.models import Foobar


@pytest.mark.django_db
def test_if_django_picks_up_created_objects(client):
    """Everything looks bright for the first test case. Database was
    initialized (conftest.py:django_db_setup) and fixtures are available"""
    TEST_STR = "hey there"

    Foobar.objects.create(name=TEST_STR)

    res = client.get("/")

    assert TEST_STR in [x.name for x in Foobar.objects.all()]
    assert TEST_STR in res.content.decode(res.charset)
    assert SESSION_FIXTURE in res.content.decode(res.charset)


@pytest.mark.django_db
def test_if_django_picks_up_initial_data(client):
    """... but, after first test case was run, there is no content
    in the database. This will fail. """

    res = client.get("/")
    assert SESSION_FIXTURE in res.content.decode(res.charset)


@pytest.mark.django_db
def test_if_django_picks_up_initial_data_for_second_time(client):
    """Let's make sure that this will fail too"""
    res = client.get("/")
    assert SESSION_FIXTURE in res.content.decode(res.charset)


@pytest.mark.django_db
def test_if_django_picks_up_database_changes(client):
    """And, now, let's check if the Django server picks up database changes"""
    TEST_STR = "5018gquafd"
    f = Foobar.objects.create(name=TEST_STR)

    res = client.get("/")
    assert TEST_STR in res.content.decode(res.charset)

    SECOND_TEST_STR = "second-test-str"

    f.name = SECOND_TEST_STR
    f.save()

    res = client.get("/")
    assert SECOND_TEST_STR in res.content.decode(res.charset)
