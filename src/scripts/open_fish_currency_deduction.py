import time

import uiautomator2
from scripts.common.extra_operation import ExtraOperation
from scripts.common.find_most_like_elem import find_most_like_elem
from scripts.common.swipe_util import swipe_already_end
from scripts.elem_img import TemplatePath
from settings import APPNAME
from uiautomator2 import Device
from uiautomator2.exceptions import UiObjectNotFoundError, XPathElementNotFoundError


class OpenFishCurrencyDeduction:
    def __init__(self, d: Device):
        """
        对一个设备上所有商品开启闲鱼币抵扣 (如果可以开启)

        :param d: 设备实例
        """
        self.d = d

    def run(self) -> tuple[bool, str]:
        """
        开始执行 开启闲鱼币抵扣 任务
        """
        with ExtraOperation(self.d):
            return self.__run()

    def __run(self) -> tuple[bool, str]:
        self.d.app_stop(APPNAME)
        self.d.app_start(APPNAME)

        try:
            return self.__开启闲鱼币抵扣()

        except UiObjectNotFoundError as e:
            return False, f'未找到元素 {e}'

        except XPathElementNotFoundError as e:
            return False, f'未找到元素 {e}'

    def __开启闲鱼币抵扣(self) -> tuple[bool, str]:
        self.d.xpath('//*[@text="我的"]').parent().click()

        # 如果开通了鱼小铺会有个工作台, 看不到 `每天免费加曝光界面`, 需要下滑一下, 这里直接滑倒底部, 等两秒弹簧动画消失
        self.d(scrollable=True).scroll.toEnd()
        time.sleep(2)

        self.d(description='每天免费加曝光').click()

        self.d(text='去设置').click()

        # 等待数据加载完成
        self.d(text='昨日数据待更新').wait()
        self.d(text='昨日数据待更新').wait_gone()

        time.sleep(2)

        first_loop = True
        while True:
            if first_loop:
                first_loop = False

            # 这里会获取到不可见的元素, 高度被设为 2px, 但元素存在
            all_10_btn = self.d.xpath('//*[@text="10%"]').all()
            all_open_btn = self.d.xpath('//*[@text="立即开启"]').all()

            # 先过滤一下, 阈值设为 15px, 只有大于这个高度的才被保留
            __threshold = 15
            all_10_btn = [i for i in all_10_btn if i.bounds[3] - i.bounds[1] > __threshold]
            all_open_btn = [i for i in all_open_btn if i.bounds[3] - i.bounds[1] > __threshold]

            # 执行一次向上滑动后(就是: 第二次进入while True循环), 有的按钮会跑到标题横幅后面, 为防止出现意外点击, 把这些也过滤掉, 也就是只保留 top >= title_elem_bottom 的按钮
            if not first_loop:
                ok, title_elem_info = find_most_like_elem(self.d.screenshot(), TemplatePath.闲鱼币抵扣界面的标题)
                if ok:
                    title_elem_bottom = title_elem_info.bounds[3]
                    all_10_btn = [i for i in all_10_btn if i.bounds[1] >= title_elem_bottom]
                    all_open_btn = [i for i in all_open_btn if i.bounds[1] >= title_elem_bottom]

            # 上滑时会出现发布宝贝的按钮
            ok, publish_btn_info = find_most_like_elem(self.d.screenshot(), TemplatePath.开启闲鱼币抵扣界面的发布宝贝按钮)

            # 如果有这个按钮, 则只点击这个按钮上方的的 `10%` 和 `开启抵扣` 按钮, 也就是只保留 bottom <= publish_button_top 的按钮
            if ok:
                publish_button_top = publish_btn_info.bounds[1]

                all_10_btn = [btn for btn in all_10_btn if btn.bounds[3] <= publish_button_top]
                all_open_btn = [btn for btn in all_open_btn if btn.bounds[3] <= publish_button_top]

            for btn_10 in all_10_btn:
                btn_10.click()
                time.sleep(1)

            for btn_open in all_open_btn:
                btn_open.click()
                # 等待开启成功弹窗出现再消失
                self.d(text='抵扣比例开启成功').wait()
                self.d(text='抵扣比例开启成功').wait_gone()
                time.sleep(1)

            # 滑动到最底部才退出循环
            if swipe_already_end(self.d, lambda: self.d.swipe(0.5, 0.7, 0.5, 0.2)):
                break

        return True, ''

    def clear(self):
        """
        该任务无需清理
        """


if __name__ == '__main__':
    d1 = uiautomator2.connect('192.168.1.169:5555')
    OpenFishCurrencyDeduction(d1).run()

