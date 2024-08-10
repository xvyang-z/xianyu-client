from uiautomator2 import Device
from uiautomator2.exceptions import UiObjectNotFoundError, XPathElementNotFoundError

from scripts.common.extra_operation import ExtraOperation
from settings import APPNAME


class Polish:

    def __init__(self, d: Device):
        self.d = d

    def run(self) -> tuple[bool, str]:
        """
        开始执行 一键擦亮
        """
        with ExtraOperation(self.d):
            return self.__run()

    def __run(self) -> tuple[bool, str]:
        self.d.app_stop(APPNAME)
        self.d.app_start(APPNAME)

        try:
            return self.__开始一键擦亮()

        except UiObjectNotFoundError as e:
            return False, f'未找到元素 {e}'

        except XPathElementNotFoundError as e:
            return False, f'未找到元素 {e}'

    def __开始一键擦亮(self) -> tuple[bool, str]:
        self.d.xpath('//*[@text="我的"]').parent().click()

        self.d(descriptionStartsWith='我发布的').click()

        self.d(description='一键擦亮').click()

        if not self.d(description='已连续擦亮').wait():
            return False, '点击一键擦亮后等待完成标志失败'

        return True, ''

    def clear(self):
        """
        该任务无需清理
        """
