import api
from model.task import Task
from scripts.open_fish_currency_deduction import OpenFishCurrencyDeduction
from uiautomator2 import Device


def handle_open_fish_currency_deduction(device: Device, task: Task):
    """
    开启闲鱼币抵扣的执行函数
    """

    open_fish_currency_deduction = OpenFishCurrencyDeduction(d=device)

    succsee, data = open_fish_currency_deduction.run()

    if not succsee:
        api.exec_fail(task=task, cmd_info=data)
        return

    success, info = api.success.open_fish_currency_deduction(task=task)

    return
