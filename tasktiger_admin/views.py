import datetime
import json
from collections import OrderedDict

from flask import abort, redirect, url_for
from flask_admin import BaseView, expose
from tasktiger import Task, TaskNotFound

from .integrations import generate_integrations


class TaskTigerView(BaseView):
    def __init__(self, tiger, integration_config=None, *args, **kwargs):
        """
        TaskTiger admin view.

        Args:
            tiger: TaskTiger instance
            integration_config: List of tuples containing integration name and
                URL
        """
        super().__init__(*args, **kwargs)
        self.tiger = tiger
        self.integration_config = (
            {} if integration_config is None else integration_config
        )

    @expose("/")
    def index(self):
        queue_stats = self.tiger.get_queue_stats()
        sorted_stats = sorted(queue_stats.items(), key=lambda k: k[0])
        groups = OrderedDict()
        for queue, stats in sorted_stats:
            queue_base = queue.split(".")[0]
            if queue_base not in groups:
                groups[queue_base] = []
            groups[queue_base].append((queue, stats))

        queue_stats_groups = []
        for group_name, queue_stats in groups.items():
            group_stats = {}
            for _, stats in queue_stats:
                for stat_name, stat_num in stats.items():
                    if stat_name not in group_stats:
                        group_stats[stat_name] = stat_num
                    else:
                        group_stats[stat_name] += stat_num
            queue_stats_groups.append((group_name, group_stats, queue_stats))

        return self.render(
            "tasktiger_admin/tasktiger.html",
            queue_stats_groups=queue_stats_groups,
        )

    @expose("/<queue>/<state>/retry/", methods=["POST"])
    def task_retry_multiple(self, queue, state):
        limit = 50
        n, tasks = Task.tasks_from_queue(self.tiger, queue, state, limit=limit)
        for task in tasks:
            task.retry()
        return redirect(url_for(".queue_detail", queue=queue, state=state))

    @expose("/<queue>/<state>/<task_id>/")
    def task_detail(self, queue, state, task_id):
        limit = 1000
        try:
            task = Task.from_id(
                self.tiger, queue, state, task_id, load_executions=limit
            )
        except TaskNotFound:
            abort(404)

        executions_dumped = []
        for execution in task.executions:
            traceback = execution.pop("traceback", None)
            execution_integrations = generate_integrations(
                self.integration_config.get("EXECUTION_INTEGRATION_LINKS", []),
                task,
                execution,
            )
            execution_converted = convert_keys_to_datetime(
                execution, ["time_failed", "time_started"]
            )
            executions_dumped.append(
                (
                    json.dumps(
                        execution_converted,
                        indent=2,
                        sort_keys=True,
                        default=str,
                    ),
                    traceback,
                    execution_integrations,
                    execution_converted,
                )
            )

        integrations = generate_integrations(
            self.integration_config.get("INTEGRATION_LINKS", []), task, None
        )

        return self.render(
            "tasktiger_admin/tasktiger_task_detail.html",
            queue=queue,
            state=state,
            task=task,
            task_data=task.data,
            task_data_dumped=json.dumps(task.data, indent=2, sort_keys=True),
            executions_dumped=reversed(executions_dumped),
            integrations=integrations,
        )

    @expose("/<queue>/<state>/<task_id>/retry/", methods=["POST"])
    def task_retry(self, queue, state, task_id):
        try:
            task = Task.from_id(self.tiger, queue, state, task_id)
        except TaskNotFound:
            abort(404)
        task.retry()
        return redirect(url_for(".queue_detail", queue=queue, state=state))

    @expose("/<queue>/<state>/<task_id>/delete/", methods=["POST"])
    def task_delete(self, queue, state, task_id):
        try:
            task = Task.from_id(self.tiger, queue, state, task_id)
        except TaskNotFound:
            abort(404)
        task.delete()
        return redirect(url_for(".queue_detail", queue=queue, state=state))

    @expose("/<queue>/<state>/")
    def queue_detail(self, queue, state):
        n, tasks = Task.tasks_from_queue(
            self.tiger, queue, state, load_executions=1
        )

        return self.render(
            "tasktiger_admin/tasktiger_queue_detail.html",
            queue=queue,
            state=state,
            n=n,
            tasks=tasks,
        )


def convert_keys_to_datetime(dict_arg, keys):
    new_dict = {**dict_arg}
    for key in keys:
        if key in new_dict:
            new_dict[key] = datetime.datetime.utcfromtimestamp(new_dict[key])
    return new_dict
