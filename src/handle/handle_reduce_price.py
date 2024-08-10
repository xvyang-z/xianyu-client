import api
from model.task import Task
from scripts.reduce_price import ReducePrice
from uiautomator2 import Device


def handle_reduce_price(device: Device, task: Task):
    """
    商品降价的执行函数
    """

    cmd_args = task.cmd_args

    price: float = cmd_args['price']
    desc: str = cmd_args['desc']

    reduce_price = ReducePrice(d=device, price=price, desc=desc)

    succsee, new_price = reduce_price.run()

    if not succsee:
        api.exec_fail(task=task, cmd_info=new_price)
        return

    success, info = api.success.reduce_price(task=task, new_price=new_price)

    return
