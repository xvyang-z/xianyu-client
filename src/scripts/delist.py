import time
from typing import Union

import uiautomator2
from uiautomator2 import Device, UiObject
from uiautomator2.exceptions import UiObjectNotFoundError, XPathElementNotFoundError

from scripts.common.extra_operation import ExtraOperation
from scripts.common.click_my_mypublish_page_search_edit_and_input import click_my_mypublish_page_search_edit_and_input
from scripts.common.get_product_desc import get_product_desc
from settings import APPNAME


class Delist:
    def __init__(self, d: Device, price: float, desc: str):
        """
        通过价格和描述一起定位一个商品

        :param d: 设备实例
        :param price: 要下架的商品的价格
        :param desc: 要下架的商品的描述
        """
        self.d = d

        self.price = price
        self.desc = desc

    def run(self) -> tuple[bool, str]:
        """
        开始执行下架任务
        """
        with ExtraOperation(self.d):
            return self.__run()

    def __run(self) -> tuple[bool, str]:
        self.d.app_stop(APPNAME)
        self.d.app_start(APPNAME)

        try:
            return self.__开始下架()
        except UiObjectNotFoundError as e:
            return False, f'未找到元素 {e}'

        except XPathElementNotFoundError as e:
            return False, f'未找到元素 {e}'

    def __开始下架(self) -> tuple[bool, str]:
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

                self.d(description='管理').click()

                self.d(description='下架').click()

                if self.d(description='确定要下架这个宝贝吗？').wait():
                    self.d(description='确定').click()
                else:
                    return False, '等待确认下架弹窗时超时'

                # 下架后会回跳到搜索页, 但搜索结果不会刷新
                # 再次点进去如果管理中有重新上架即可证明操作成功
                time.sleep(2)
                i.click()
                self.d(description='管理').click()

                if self.d(description='重新发布').wait():
                    return True, ''
                else:
                    return False, '点击下架了但没下架成功'

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
    device = uiautomator2.connect('192.168.31.69:5555')
    device.settings['wait_timeout'] = 10.0  # 测试, 将超时时间设个小值, 方便快速调试, 原值是 20.0

    delist = Delist(
        d=device,
        price=9999999.00001,
        desc='5KcM',
    )

    print(delist.run())

    delist.clear()
