import api
from model.task import Task
from scripts.crawl import Crawl
from uiautomator2 import Device


def handle_crawl(device: Device, task: Task):
    """
    爬取任务的执行函数
    """
    cmd_args = task.cmd_args

    keyword = cmd_args['keyword']

    crawl = Crawl(d=device, key=keyword)

    succsee, data = crawl.run()

    if not succsee:
        api.exec_fail(task=task, cmd_info=data)
        return

    # 先上传爬到的图片
    success, info = api.upload_file(data)

    # 图片上传后不管执行成功与否都清理
    crawl.clear()

    if not success:
        api.exec_fail(task=task, cmd_info=info)
        return

    # 再上报任务完成, 更新任务状态
    success, info = api.success.crawl(task=task, products=data)

    if not success:
        api.exec_fail(task=task, cmd_info=info)
        return

    return
