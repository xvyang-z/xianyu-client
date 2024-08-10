import json

import requests
from model.task import Cmd
from requests.exceptions import ConnectionError

from db import Session, ReRequest
from model.task import Task
from settings import CLIENT_API, API_HEADER
from util.request_lock import request_lock


@request_lock
def base_request(task: Task, json_data: dict) -> tuple[bool, str]:
    """
    :param task: 任务对象
    :param json_data: 请求时的json信息
    """

    url = CLIENT_API + task.cmd.success_route

    try:
        resp = requests.post(
            url=url,
            headers=API_HEADER,
            json=json_data
        )

        resp_json = resp.json()
        if resp_json['code'] == 0:
            return True, ''
        else:
            return False, resp_json['message']

    except ConnectionError as e:
        # 网络出错, 暂存任务, 下次获取任务前提交系统同步数据
        # 爬取商品这个任务不涉及到发布管理的同步, 这里如果上报失败不存储他的执行成功状态, 服务端检测到他超时会设为执行超时状态, 会再次下发任务重新爬取
        if task.cmd == Cmd.爬取商品:
            return False, str(e)

        with Session() as session:
            # 当某个任务因网络问题执行失败, 下次重试时网络不恢复会再次进到这个 except 块中, 为了避免重复添加, 这里先进行一次检测
            if session.query(ReRequest).get(task.task_id) is None:
                session.add(
                    ReRequest(
                        task_id=task.task_id,
                        task_str=task.to_json_str(),
                        json_data_str=json.dumps(json_data)
                    )
                )

            session.commit()

        return False, str(e)
