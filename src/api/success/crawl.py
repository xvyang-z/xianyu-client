from api.success.base_request import base_request
from model.task import Task
from model.product import Product


def crawl(task: Task, products: list[Product]) -> tuple[bool, str]:
    """
    爬取数据成功 且 图片上传完, 再调用这个接口
    """
    products2 = []
    for product in products:
        products2.append({
            'uuid': product.product_uuid,
            'desc': product.desc,
            'images': product.remote_img_path,
            'price': product.price
        })

    return base_request(
        task=task,
        json_data={
            'task_id': task.task_id,
            'products': products2
        }
    )
