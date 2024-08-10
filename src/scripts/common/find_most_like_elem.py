import cv2
import numpy as np
from PIL.Image import Image

from scripts.elem_img import TemplatePath


class Elem_Info:
    def __init__(self, center_x: int, center_y: int, left: int, top: int, right: int, bottom: int):
        self.center = (center_x, center_y)
        self.bounds = (left, top, right, bottom)


def find_most_like_elem(screen_shot: Image, template_path: TemplatePath) \
        -> tuple[bool, Elem_Info]:
    """
    在 screen_shot 中找到和模板 template_path 最匹配的元素的 中心点 边界信息

    :param screen_shot: 截图, Device.screenshot() 或 UIObject.screenshot() 默认返回的 Image 格式
    :param template_path: 模板文件路径, 模板是从 (1080, 2340) 分辨率手机上截屏扣出来的, 统一在 ROOT_DIR/scripts/elem_img/__init__.py:template_path中写明
    """
    screen_shot = np.array(screen_shot)

    height, width, n = screen_shot.shape

    # 模板图像是在 1080 宽的手机上截屏裁取的, 这里以 1080 为基准, 对截屏图片的大小进行等比缩放, 去除不同分辨率影响
    scale = 1080 / width

    new_width = 1080
    new_height = int(scale * height)

    screen_shot = cv2.resize(
        screen_shot,
        dsize=(new_width, new_height),
        interpolation=cv2.INTER_LINEAR
    )

    template = cv2.imread(str(template_path.value))
    template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)

    result = cv2.matchTemplate(
        image=screen_shot,
        templ=template,
        method=cv2.TM_CCOEFF_NORMED  # 这种模式适合精确匹配
    )

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(max_val)
    # 符合度过低则认为没找到这个元素
    if max_val < 0.85:  # todo 配置项
        return False, Elem_Info(0, 0, 0, 0, 0, 0)

    left = max_loc[0]
    top = max_loc[1]
    right = max_loc[0] + template.shape[1]
    bottom = max_loc[1] + template.shape[0]

    # 这里计算的是重设大小后的图片的坐标, 还要根据比例转换成原始图片上的坐标
    src_left = int(left / scale)
    src_top = int(top / scale)
    src_right = int(right / scale)
    src_bottom = int(bottom / scale)

    src_center_x = int((left + right) / 2)
    src_center_y = int((top + bottom) / 2)

    return True, Elem_Info(src_center_x, src_center_y, src_left, src_top, src_right, src_bottom)


if __name__ == '__main__':
    import uiautomator2 as u2

    d = u2.connect('192.168.31.69:5555')

    i = d(descriptionContains='降价')
    print(i.bounds())
    print(
        find_most_like_elem(
            screen_shot=i.screenshot(),
            template_path=TemplatePath.降价按钮,
        )
    )
