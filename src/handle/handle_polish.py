import api
from model.task import Task
from scripts.polish import Polish
from uiautomator2 import Device


def handle_polish(device: Device, task: Task):
    """
    一键擦亮 任务的执行函数
    """

    polish = Polish(d=device)

    succsee, data = polish.run()

    if not succsee:
        api.exec_fail(task=task, cmd_info=data)
        return

    success, info = api.success.delete(task=task)

    return
