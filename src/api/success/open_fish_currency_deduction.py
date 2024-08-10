from api.success.base_request import base_request
from model.task import Task


def open_fish_currency_deduction(task: Task) -> tuple[bool, str]:
    return base_request(
        task=task,
        json_data={
            'task_id': task.task_id,
        }
    )
