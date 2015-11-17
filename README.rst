===============
tasktiger-admin
===============

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
