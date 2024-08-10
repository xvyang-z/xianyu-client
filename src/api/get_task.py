from typing import Union

import requests

from model.task import Task
from model.task import Cmd
from settings import CLIENT_API, API_HEADER
from util.request_lock import request_lock



class Data:
    cmd: str
    task_id: int
    device_flag: str
    device_name: str
    is_open_fish_shop: bool
    cmd_args: dict



@request_lock
def get_task() -> tuple[bool, Union[list[Task], str]]:
    """
    客户端执行某项任务失败调这个接口返回给服务器出错的具体信息
    """
    try:
        resp = requests.post(
            url=f'{CLIENT_API}/get_task',
            headers=API_HEADER,
        )

        resp_json = resp.json()
        if resp_json['code'] == 0:
            tasks = []
            for t in resp_json['data']:

                cmd = Cmd.from_str(t['cmd'])

                task = Task(
                    task_id=t['task_id'],
                    device_flag=t['device_flag'],
                    device_name=t['device_name'],
                    is_open_fish_shop=t['is_open_fish_shop'],
                    cmd=cmd,
                    cmd_args=t['cmd_args'],
                )

                tasks.append(task)

            return True, tasks

        else:
            return False, resp_json['message']

    except Exception as e:
        return False, str(e)
