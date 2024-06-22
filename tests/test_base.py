import datetime

import redis
from flask import Flask
from flask_admin import Admin
from tasktiger import TaskTiger, Worker

from tasktiger_admin import TaskTigerView

from .config import REDIS_HOST, TEST_DB

conn = redis.Redis(host=REDIS_HOST, db=TEST_DB, decode_responses=True)
tiger = TaskTiger(setup_structlog=True, connection=conn)


@tiger.task
def simple_task():
    pass


class BaseTestCase:
    def setup_method(self, method):
        conn.flushdb()

        self.flask_app = Flask("Test App")
        self.flask_app_admin = Admin(self.flask_app, url="/")
        self.flask_app_admin.add_view(
            TaskTigerView(tiger, name="TaskTiger", endpoint="tasktiger")
        )
        self.client = self.flask_app.test_client()

    def teardown_method(self, method):
        conn.flushdb()


class EagerExecution:
    def __enter__(self):
        self.original_value = tiger.config["ALWAYS_EAGER"]
        tiger.config["ALWAYS_EAGER"] = True

    def __exit__(self, type, value, traceback):
        tiger.config["ALWAYS_EAGER"] = self.original_value


class TestCase(BaseTestCase):
    def test_basic(self):
        # create a few executed, scheduled, and queued tasks

        # create executed tasks
        with EagerExecution():
            simple_task.delay()
            simple_task.delay()
            Worker(tiger).run(once=True)

        # create scheduled tasks
        tiger.delay(simple_task, when=datetime.timedelta(seconds=30))
        tiger.delay(simple_task, when=datetime.timedelta(seconds=30))
        tiger.delay(simple_task, when=datetime.timedelta(seconds=30))

        # create queued tasks (no worker is picking this up)
        simple_task.delay()

        # do a simple get request
        response = self.client.get("/")
        assert response.status_code == 200
        assert b"TaskTiger" in response.data
