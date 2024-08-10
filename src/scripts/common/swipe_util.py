import time
from typing import Callable

from uiautomator2 import Device, UiObject


def swipe_until_find_elem(d: Device, elem: UiObject, swipe_func: Callable):
    """
    滚动直到找到某个元素出现, 滚动到最后还找不到会返回 False
    仅适用于有限的滚动列表 !!!
    不能用在无限加载的滚动列表 !!!

    :param d: 设备实例
    :param elem: 元素选择器
    :param swipe_func: 滑动函数, 形如 lambda: d.swipe(0.5, 0.5, 0.5, 0.25, steps=100)
    """

    # 如果不存在就一直滚动, 直到最后
    while not elem.exists:
        if swipe_already_end(d, swipe_func):
            break

    return elem.exists


def swipe_already_end(d: Device, swipe_func: Callable) -> bool:
    """
    执行一次给定的 swipe_func, 滑动前后界面结构相同则返回 True, 否则返回 False

    :param d: 设备实例
    :param swipe_func: 滑动函数, 形如 lambda: d.swipe(0.5, 0.5, 0.5, 0.25, steps=100)
    """
    # 在dump前等待一下, 等待弹簧动画过后再检查
    # 如果在弹簧动画持续时间内dump, 获取到的永远也不相同
    time.sleep(1)
    before_swipe_page = d.dump_hierarchy()

    swipe_func()

    time.sleep(1)
    after_swipe_page = d.dump_hierarchy()

    if before_swipe_page == after_swipe_page:
        return True
    else:
        return False
