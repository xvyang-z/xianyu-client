import api
from model.task import Task
from scripts.republish import RePublish
from uiautomator2 import Device


def handle_republish(device: Device, task: Task):
    """
    下架商品的执行函数
    """

    cmd_args = task.cmd_args

    price: float = cmd_args['price']
    desc: str = cmd_args['desc']

    rp = RePublish(d=device, price=price, desc=desc)

    succsee, data = rp.run()

    if not succsee:
        api.exec_fail(task=task, cmd_info=data)
        return

    success, info = api.success.republish(task=task)

    return
