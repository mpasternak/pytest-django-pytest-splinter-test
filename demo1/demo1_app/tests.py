from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.ui import WebDriverWait

from demo1_app.conftest import SESSION_FIXTURE
from demo1_app.models import Foobar


class wait_for_page_load(object):
    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_by_tag('html')[0]._element

    def __exit__(self, *_):
        WebDriverWait(self.browser, 10).until(
            staleness_of(self.old_page)
        )


def test_if_liveserver_picks_up_created_objects(live_server, browser):
    """Everything looks bright for the first test case. Database was
    initialized (conftest.py:django_db_setup) and fixtures are available"""
    TEST_STR = "hey there"

    Foobar.objects.create(name=TEST_STR)

    with wait_for_page_load(browser):
        browser.visit(live_server.url)

    assert TEST_STR in [x.name for x in Foobar.objects.all()]
    assert TEST_STR in browser.html
    assert SESSION_FIXTURE in browser.html


def test_if_liveserver_picks_up_initial_data(live_server, browser):
    """... but, after first test case was run, there is no content
    in the database. This will fail. """
    with wait_for_page_load(browser):
        browser.visit(live_server.url)

    assert SESSION_FIXTURE in browser.html


def test_if_liveserver_picks_up_initial_data_for_second_time(
        live_server, browser):
    """Let's make sure that this will fail too"""
    with wait_for_page_load(browser):
        browser.visit(live_server.url)

    assert SESSION_FIXTURE in browser.html



def test_if_liveserver_picks_up_database_changes(
        live_server, browser):
    """And, now, let's check if the LiveServer picks up database changes"""
    TEST_STR = "5018gquafd"
    f = Foobar.objects.create(name=TEST_STR)

    with wait_for_page_load(browser):
        browser.visit(live_server.url)

    assert TEST_STR in browser.html

    SECOND_TEST_STR = "second-test-str"

    f.name = SECOND_TEST_STR
    f.save()

    with wait_for_page_load(browser):
        browser.visit(live_server.url)

    assert SECOND_TEST_STR in browser.html



