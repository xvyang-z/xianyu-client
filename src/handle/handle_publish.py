import api
from model.task import Task
from scripts.publish import Publish
from uiautomator2 import Device


def handle_publish(device: Device, task: Task):
    """
    发布商品的执行函数
    """

    cmd_args = task.cmd_args

    uuid: str = cmd_args['uuid']
    price: float = cmd_args['price']
    desc: str = cmd_args['desc']
    images: list[str] = cmd_args['images']
    location: list[str] = cmd_args['location']

    publish = Publish(d=device, uuid=uuid, price=price, desc=desc, images=images, location=location)

    succsee, data = publish.run()

    publish.clear()

    if not succsee:
        api.exec_fail(task=task, cmd_info=data)
        return

    success, info = api.success.publish(task=task)

    return
