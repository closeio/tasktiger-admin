import sys
import click
from flask import Flask
from flask_admin import Admin
import redis
from tasktiger import TaskTiger
from tasktiger_admin import TaskTigerView

PY2 = sys.version_info[0] == 2


@click.command()
@click.option('-h', '--host', help='Redis server hostname')
@click.option('-p', '--port', help='Redis server port')
@click.option('-a', '--password', help='Redis password')
@click.option('-n', '--db', help='Redis database number')
@click.option('-l', '--listen', help='Admin port to listen on')
def run_admin(host, port, db, password, listen):
    decode_responses = not PY2
    conn = redis.Redis(host, int(port or 6379), int(db or 0), password, decode_responses=decode_responses)
    tiger = TaskTiger(setup_structlog=True, connection=conn)
    app = Flask(__name__)
    admin = Admin(app, url='/')
    admin.add_view(TaskTigerView(tiger, name='TaskTiger', endpoint='tasktiger'))
    app.run(debug=True, port=int(listen or 5000))
