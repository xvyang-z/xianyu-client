import time

import uiautomator2
from scripts.common.extra_operation import ExtraOperation
from settings import APPNAME
from uiautomator2 import Device
from uiautomator2.exceptions import UiObjectNotFoundError, XPathElementNotFoundError


class GetCoinAndSignin:
    def __init__(self, d: Device):
        """
        :param d: 设备实例
        """
        self.d = d

    def run(self) -> tuple[bool, str]:
        """
        开始执行投骰子和签到任务
        """
        with ExtraOperation(self.d):
            return self.__run()

    def __run(self) -> tuple[bool, str]:
        self.d.app_stop(APPNAME)
        self.d.app_start(APPNAME)

        try:
            return self.__打开赚闲鱼币页面()

        except UiObjectNotFoundError as e:
            return False, f'未找到元素 {e}'

        except XPathElementNotFoundError as e:
            return False, f'未找到元素 {e}'

    def __打开赚闲鱼币页面(self):
        self.d.xpath('//*[@text="我的"]').parent().click()

        # 如果开通了鱼小铺会有个工作台, 看不到 `每天免费加曝光界面`, 需要下滑一下, 这里直接滑倒底部, 等两秒弹簧动画消失
        self.d(scrollable=True).scroll.toEnd()
        time.sleep(2)

        self.d(descriptionStartsWith='每天免费加曝光').click()

        return self.__扔骰子寻宝()

    def __扔骰子寻宝(self) -> tuple[bool, str]:
        self.d(resourceId='mapDiceBtn').wait()
        self.d(resourceId='mapDiceBtn').click()
        while True:
            # 停止执行 5 秒钟
            # time.sleep(5)
            self.d(resourceId='mapDiceBtn').wait()
            if self.d(text='明日再来') or self.d(text='签到'):
                test = True
            else:
                test = False
            if self.d(resourceId='mapDiceBtn').exists(timeout=5) and not test:
                self.d(resourceId='mapDiceBtn').click()
            else:
                break
        time.sleep(3)
        if self.d(text='签到').wait():
            self.d(text='签到').click()
            return True, ''
        else:
            return True, '今天已经签过到了'


if __name__ == '__main__':
    device = uiautomator2.connect('192.168.1.214')
    device.settings['wait_timeout'] = 10.0  # 测试, 将超时时间设个小值, 方便快速调试, 原值是 20.0
    g = GetCoinAndSignin(d=device)
    print(g.run())
