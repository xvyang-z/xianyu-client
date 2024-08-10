import requests

from model.product import Product
from settings import SERVER_HOST, API_HEADER


def upload_file(products: list[Product]) -> tuple[bool, str]:
    try:
        # 先上传爬到的所有商品图片
        for product in products:
            resp = requests.post(
                url=f'{SERVER_HOST}/upload/user_product_img',
                headers=API_HEADER,
                data={
                    "product_uuid": product.product_uuid,
                },
                files=[
                    ('files', open(img_path, 'rb')) for img_path in product.local_img_path
                ]
            )

            resp_json = resp.json()
            if resp_json['code'] == 0:
                data = resp_json['data']
                product.remote_img_path = [i['file_path'] for i in data]

            else:
                return False, f'爬取完成, 上传图片时失败 {resp_json["message"]}'

        return True, ''
    except Exception as e:
        return False, f'爬取完成, 上传图片时出错 {e}'
