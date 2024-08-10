from enum import Enum
from settings import ROOT_DIR


_elem_img_dir = ROOT_DIR / 'scripts' / 'elem_img' / 'img'


class TemplatePath(Enum):

    确认降价按钮 = _elem_img_dir / 'confirm_reduce_price_button.png'
    降价按钮 = _elem_img_dir / 'reduce_price_button.png'

    选择位置的图标 = _elem_img_dir / 'location_pin.png'

    话题标签1 = _elem_img_dir / 'label_tag_1.png'
    话题标签2 = _elem_img_dir / 'label_tag_2.png'
    话题标签3 = _elem_img_dir / 'label_tag_3.png'
    芝麻工作证 = _elem_img_dir / 'sesame_work_permit.png'

    开启闲鱼币抵扣界面的发布宝贝按钮 = _elem_img_dir / 'deduction_page_publish_button.png'
    闲鱼币抵扣界面的标题 = _elem_img_dir / 'deduction_page_title.png'
