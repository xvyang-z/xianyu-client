import api
from model.task import Task
from scripts.delete import Delete
from uiautomator2 import Device


def handle_delete(device: Device, task: Task):
    """
    删除商品的执行函数
    """

    cmd_args = task.cmd_args

    price: float = cmd_args['price']
    desc: str = cmd_args['desc']
    is_delist: bool = cmd_args['is_delist']

    delete = Delete(d=device, price=price, desc=desc, is_delist=is_delist)

    succsee, data = delete.run()

    if not succsee:
        api.exec_fail(task=task, cmd_info=data)
        return

    success, info = api.success.delete(task=task)

    return
