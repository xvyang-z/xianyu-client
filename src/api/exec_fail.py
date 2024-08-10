import requests

from model.task import Task
from settings import CLIENT_API, API_HEADER
from util.request_lock import request_lock


@request_lock
def exec_fail(task: Task, cmd_info: str):
    """
    客户端执行某项任务失败调这个接口返回给服务器出错的具体信息
    """
    try:
        resp = requests.post(
            url=f'{CLIENT_API}/exec_fail',
            headers=API_HEADER,
            json={
                'task_id': task.task_id,
                'cmd_info': cmd_info
            }
        )
        if resp.json()['code'] == 0:
            ...  # todo
        else:
            ...  # todo
    except Exception:
        ...  # todo
