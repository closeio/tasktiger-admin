===============
tasktiger-admin
===============

.. image:: https://circleci.com/gh/closeio/tasktiger-admin.svg?style=svg
    :target: https://circleci.com/gh/closeio/tasktiger-admin

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
	:target: https://github.com/psf/black

*tasktiger-admin* is an admin interface for TaskTiger_ using flask-admin. It
comes with an overview page that shows the amount of tasks in each queue for
each state (queued, active, scheduled, error). It lets you inspect queues and
individual tasks, as well as delete and retry tasks that errored out.

(Interested in working on projects like this? `Close.io`_ is looking for `great engineers`_ to join our team)

.. _TaskTiger: https://github.com/closeio/tasktiger
.. _Close.io: http://close.io
.. _great engineers: http://jobs.close.io


Quick start
-----------

.. code:: bash

  % tasktiger-admin

This will listen on the default port (5000) and connect to the default Redis
instance. Additional settings are available (see ``--help`` switch for
details).

For a more advanced integration, *tasktiger-admin* can be integrated in a Flask
app with an existing flask-admin by using the provided view in
``tasktiger_admin.views.TaskTigerView``.


Integration Links
-----------------
The ``TaskTigerView`` class takes an optional ``integration_config`` parameter
that can be used to render integration links on the admin Task Detail page.
These can be used to easily navigate to external resources like logging
infrastructure or a Wiki. ``integration_config`` should be a list of tuples
that specify the integration name and URL template.

The URL template supports three variables:

* ``task_id``: Current task id
* ``execution_start``: Execution start time minus a 10 second buffer
* ``execution_failed``: Execution failed time plus a 10 second buffer

Example integration config that points to a logging website.

.. code:: python

  integration_config = [('Logs', 'https://logs.example.com/search/?'
                                 'task_id={{ task_id }}&'
                                 'start_time={{ execution_start }}&'
                                 'end_time={{ execution_failed }}')]
