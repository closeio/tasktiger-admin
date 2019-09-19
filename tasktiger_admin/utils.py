import os

import click
import dsnparse
from flask import Flask
from flask_admin import Admin
import redis
from tasktiger import TaskTiger
from tasktiger_admin import TaskTigerView


@click.command()
@click.option('-h', '--host', help='Redis server hostname')
@click.option('-p', '--port', help='Redis server port')
@click.option('-a', '--password', help='Redis password')
@click.option('-n', '--db', help='Redis database number')
@click.option('-l', '--listen', help='Admin port to listen on')
@click.option('-i', '--interface', help='Admin interface to listen on',
              default='127.0.0.1')
@click.option(
    '--structlog/--no-structlog', default=True, help='Enable/Disable structlog'
)
def run_admin(host, port, db, password, listen, interface, **kwargs):
    environ_dsn = os.environ.get('REDIS_URL', None)
    if environ_dsn:
        dsn_parsed = dsnparse.parse(environ_dsn)
        host = host or dsn_parsed.host
        port = port or dsn_parsed.port
        password = dsn_parsed.password
    conn = redis.Redis(host, int(port or 6379), int(db or 0), password)
    tiger = TaskTiger(setup_structlog=kwargs['structlog'], connection=conn)
    app = Flask(__name__)
    admin = Admin(app, url='/')
    admin.add_view(TaskTigerView(tiger, name='TaskTiger', endpoint='tasktiger'))
    app.run(debug=False, port=int(listen or 5000), host=interface)
