import api
from model.task import Task
from scripts.delist import Delist
from uiautomator2 import Device


def handle_delist(device: Device, task: Task):
    """
    下架商品的执行函数
    """

    cmd_args = task.cmd_args

    price: float = cmd_args['price']
    desc: str = cmd_args['desc']

    delist = Delist(d=device, price=price, desc=desc)

    succsee, data = delist.run()

    if not succsee:
        api.exec_fail(task=task, cmd_info=data)
        return

    success, info = api.success.delist(task=task)

    return
