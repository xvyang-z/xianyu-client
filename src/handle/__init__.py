import json
import threading
import time
from queue import Queue

import uiautomator2
from uiautomator2 import ConnectError

from api import exec_fail, get_task
from db import Session, ReRequest
from handle.handle_crawl import handle_crawl
from handle.handle_delete import handle_delete
from handle.handle_delist import handle_delist
from handle.handle_publish import handle_publish
from handle.handle_reduce_price import handle_reduce_price
from handle.handle_republish import handle_republish
from model.task import Task
from settings import SLEEP_TIME
from util.connect_state import ConnectState


# 每个线程跑一个这个函数
def device_exec_task_queue(device_flag: str, task_queue: Queue[Task]):
    """
    每个设备都会创建一个这个函数, 阻塞地监听自己的任务列表
    """

    while True:
        device_thread_running[device_flag] = False

        task = task_queue.get()  # 阻塞地获取

        device_thread_running[device_flag] = True

        # 某个任务执行失败就跳过, 执行其他的
        try:
            # 每次执行前都连接一下
            device = uiautomator2.connect(device_flag)

            # 执行对应的函数
            task.cmd.handle_func(device, task)

        except ConnectError:
            exec_fail(task, '设备连接失败')

        except Exception as e:
            exec_fail(task, f'未知错误 {e}')


def re_request_task_by_net_error() -> tuple[bool, str]:
    """
    重新上报: 脚本执行成功, 但上报进度时网络出错的任务

    :return: 如果本地没有这种任务直接返回 True
    """
    with Session() as session:
        re_reqs = session.query(ReRequest).all()

        if len(re_reqs) == 0:
            return True, '无需要重传的数据'

        for re_req in re_reqs:
            success, info = success.base_request(
                task=Task.from_json_str(re_req.task_str),
                json_data=json.loads(re_req.json_data_str)
            )

            if success:
                session.delete(re_req)

            try:
                session.commit()
            except Exception as e:
                session.rollback()
                return False, f'数据重传失败 {e}'


def handle_start():

    # 每次获取任务前, 先看本地是否有执行成功但上报出错的任务, 有的话就先同步数据, 直到全部完成
    while True:
        ConnectState.update(False, '数据重传中...')

        ok, info = re_request_task_by_net_error()

        ConnectState.update(ok, info)

        if ok:
            break

        time.sleep(SLEEP_TIME)

    while True:

        ConnectState.update(False, '获取任务中...')

        ok, tasks = get_task()
        if not ok:
            ConnectState.update(False, tasks)
            time.sleep(SLEEP_TIME)
            continue

        ConnectState.update(True, '连接正常')

        for TASK in tasks:
            d_flag = TASK.device_flag
            d_name = TASK.device_name

            # 初始化运行状态为 False
            if device_thread_running.get(d_flag) is None:
                device_thread_running[d_flag] = False

            if device_flag_to_name.get(d_flag) is None:
                device_flag_to_name[d_flag] = d_name

            # 将获取到的任务放到对应设备的任务队列中
            if device_task_queue.get(d_flag) is None:
                device_task_queue[d_flag] = Queue()
                device_task_queue[d_flag].put(TASK)
            else:
                device_task_queue[d_flag].put(TASK)

            # 看有没有新设备任务需要创建线程去执行
            if device_thread.get(d_flag) is None:
                device_thread[d_flag] = threading.Thread(
                    target=device_exec_task_queue,
                    args=(d_flag, device_task_queue[d_flag]),
                )
                device_thread[d_flag].start()

        time.sleep(SLEEP_TIME)


# 将每个设备的任务放到一个列表中, 再开线程去执行, 每个设备同一时间仅能执行一个任务
device_task_queue: dict[str, Queue[Task]] = {}

# 设备的线程
device_thread: dict[str, threading.Thread] = {}

# 设备是否在运行任务标识, 用于退出 gui 时提示, 保证任务尽量能够正常完成一个完整流程, 防止数据错乱
device_thread_running: dict[str, bool] = {}

# 设备标识 对应的 设备名, 给 gui 显示
device_flag_to_name: dict[str, str] = {}
