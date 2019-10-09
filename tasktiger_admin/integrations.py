import datetime

import jinja2

TIME_BUFFER = 10  # Number of seconds to buffer start/end times


def _get_template_vars(task, execution):
    info = {}
    if task:
        info['task_id'] = task.id

    if execution:
        info['execution_start'] = _get_time(
            execution['time_started'], -TIME_BUFFER
        )
        info['execution_failed'] = _get_time(
            execution['time_failed'], TIME_BUFFER
        )

    return info


def _get_time(time_string, delta):
    execution_time = datetime.datetime.utcfromtimestamp(
        int(time_string) + delta
    )
    return execution_time.isoformat()


def generate_integrations(integration_templates, task, execution):
    """
    Generate integration URLs.

    Args:
        task: TaskTiger task
        execution: Task execution dictionary
        integration_templates: List of integration templates

    Returns:
        list: List of tuples containing integration name and URL
    """
    integrations = []
    for name, url_template in integration_templates:
        url_template = jinja2.Template(url_template)
        url = url_template.render(**_get_template_vars(task, execution))
        integrations.append((name, url))
    return integrations
