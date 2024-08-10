from pathlib import Path


class Product:
    def __init__(
            self,
            product_uuid: str,
            price: float,
            desc: str,
            local_img_path: list[Path],

            remote_img_path: list[str] = None,
    ):

        # 本地生成
        self.product_uuid = product_uuid
        self.price = price
        self.desc = desc
        self.local_img_path = local_img_path

        # 上传图片后会获取到远程图片的路由, 再给这个属性赋值
        self.remote_img_path = remote_img_path
