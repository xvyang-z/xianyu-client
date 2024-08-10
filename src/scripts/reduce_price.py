import time
from typing import Union

import uiautomator2
from uiautomator2 import Device, UiObject
from uiautomator2.exceptions import UiObjectNotFoundError, XPathElementNotFoundError

from scripts.common.extra_operation import ExtraOperation
from scripts.common.click_my_mypublish_page_search_edit_and_input import click_my_mypublish_page_search_edit_and_input
from scripts.common.find_most_like_elem import find_most_like_elem
from scripts.common.get_product_desc import get_product_desc
from scripts.elem_img import TemplatePath
from settings import APPNAME


class ReducePrice:
    def __init__(self, d: Device, price: float, desc: str):
        """
        通过价格和描述一起定位一个商品

        :param d: 设备实例
        :param price: 要降价的商品的价格
        :param desc: 要降价的商品的描述
        """
        self.d = d

        self.price = price
        self.desc = desc

    def run(self) -> tuple[bool, Union[float, str]]:
        """
        开始执行降价任务
        """
        with ExtraOperation(self.d):
            return self.__run()

    def __run(self) -> tuple[bool, str]:
        self.d.app_stop(APPNAME)
        self.d.app_start(APPNAME)

        try:
            return self.__开始降价()
        except UiObjectNotFoundError as e:
            return False, f'未找到元素 {e}'

        except XPathElementNotFoundError as e:
            return False, f'未找到元素 {e}'

    def __开始降价(self) -> tuple[bool, Union[float, str]]:
        self.d.xpath('//*[@text="我的"]').parent().click()

        self.d(descriptionStartsWith='我发布的').click()

        success, search_elem = click_my_mypublish_page_search_edit_and_input(self.d, self.desc)
        if not success:
            search_elem: str
            return False, search_elem

        search_elem: Union[UiObject, list[UiObject]]

        while True:
            for i in search_elem:

                # 这个商品元素是一整个块, 信息都在一个字符串里, 通过 换行符 分割
                product_info: list[str] = i.info['contentDescription'].split('\n')

                # 如果是整数金额 则 [5] 是价格
                _price = product_info[5]

                # 如果是小数, 则 [6] 是以小数点开头的, 拼接一下形成完整价格
                if product_info[6].startswith('.'):
                    _price += product_info[6]

                # 这里不用相等判断, 价格之差大于等于 0.01 认为价格不同
                if abs(float(_price) - self.price) >= 0.01:
                    continue

                # 点进去对比描述信息
                i.click()

                success, _desc = get_product_desc(self.d)
                if not success:
                    self.d.press('back')
                    time.sleep(2)
                    continue

                # 在发布时可能会在最后加上个 `\n感兴趣的话点"我想要"和我私聊吧~`, 用 startswith 比较
                if not _desc.startswith(self.desc):
                    self.d.press('back')
                    time.sleep(2)
                    continue

                # 到这里说明对比成功, 返回搜索界面去点击降价按钮
                self.d.press('back')
                time.sleep(2)

                # 找到 降价按钮 相对于 这个块 的坐标
                success, elem_info = find_most_like_elem(screen_shot=i.screenshot(), template_path=TemplatePath.降价按钮)
                if not success:
                    return False, '找到了对应商品元素, 但未找到降价按钮, 可能图片匹配的阈值过高'

                x, y = elem_info.center
                lt_x, lt_y, _, _ = i.bounds()

                # 点击降价按钮
                self.d.click(x=lt_x + x, y=lt_y + y)

                # 等待确认降价的弹窗出现
                self.d(description='确认降价').wait()

                # 此时不对降价金额做修改, 使用默认的降价金额(9折), 直接点击确认降价
                # 但如果此时金额 <= 16, 不会默认的在弹窗界面设置为9折 (已在服务端判断)

                # 找到 确认降价按钮 相对于 屏幕 坐标
                success, elem_info = find_most_like_elem(screen_shot=self.d.screenshot(), template_path=TemplatePath.确认降价按钮)
                if not success:
                    return False, '点击了降价按钮, 但未找到弹窗中的确认降价按钮, 可能图片匹配的阈值过高'

                x, y = elem_info.center
                # 点击确认降价按钮
                self.d.click(x=x, y=y)

                # 此时会出现弹窗 '降价成功'
                if not self.d(text='降价成功').wait():
                    return False, '点击确认降价按钮后未检测到降价成功的弹窗'

                # 获取降价后的金额
                product_info: list[str] = i.info['contentDescription'].split('\n')
                _price = product_info[5]
                if product_info[6].startswith('.'):
                    _price += product_info[6]

                return True, float(_price)

            # 如果没滑倒底, 就滑动 0.7 屏, 再次遍历, 可能会对某个元素重复执行, 问题不大
            if not self.d(description='哎呀，到底啦～').exists:
                self.d.swipe(0.5, 0.8, 0.5, 0.1, steps=200)
                continue

            return False, '未找到符合描述和价格的商品'  # 如果到底了, 还没找到合适的

    def clear(self):
        """
        该任务无需清理
        """


if __name__ == '__main__':
    device = uiautomator2.connect('192.168.1.214:5555')
    device.settings['wait_timeout'] = 10.0  # 测试, 将超时时间设个小值, 方便快速调试, 原值是 20.0

    rp = ReducePrice(
        d=device,
        price=580,
        desc='python自动化开发接单',
    )

    print(rp.run())

    rp.clear()
