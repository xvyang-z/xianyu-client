from api.success.base_request import base_request
from model.task import Task


def reduce_price(task: Task, new_price: float) -> tuple[bool, str]:
    return base_request(
        task=task,
        json_data={
            'task_id': task.task_id,
            'new_price': new_price
        }
    )
