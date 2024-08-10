import time

import uiautomator2
from uiautomator2 import Device


class ExtraOperation:
    """
    附加操作
    """
    def __init__(self, d: Device):
        self.d = d

        self.ctx = self.d.watch_context()

        # 遇到权限时, 点击允许
        self.ctx.when("com.lbe.security.miui:id/permission_allow_foreground_only_button").click()

        # 遇到更新时, 点击暂不升级
        self.ctx.when('亲，有新版本可以升级了').when('暂不升级').click()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ctx.stop()


if __name__ == '__main__':
    d1 = uiautomator2.connect('192.168.31.48:5555')
    with ExtraOperation(d1):
        time.sleep(20)
