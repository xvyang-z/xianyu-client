import api
from model.task import Task
from scripts.get_coin_and_signin import GetCoinAndSignin
from uiautomator2 import Device


def handle_get_coin_and_signin(device: Device, task: Task):
    """
    签到闲鱼币 的执行函数
    """

    gcas = GetCoinAndSignin(d=device)

    succsee, data = gcas.run()

    if not succsee:
        api.exec_fail(task=task, cmd_info=data)
        return

    success, info = api.success.get_coin_and_sigin(task=task)

    return
