import os
import re
import shutil
import time
import uuid
from pathlib import Path
from typing import Union

import cv2
import numpy as np
import uiautomator2
from scripts.common.swipe_util import swipe_already_end
from uiautomator2 import Device
from uiautomator2.exceptions import UiObjectNotFoundError, XPathElementNotFoundError

from scripts.common.extra_operation import ExtraOperation
from scripts.common.get_product_desc import get_product_desc
from settings import IMG_PATH, APPNAME
from model.product import Product


class Crawl:
    def __init__(self, d: Device, key: str = None, total=5):
        """
        :param key: 爬取关键字
        :param total: 爬取条数
        """
        self.d = d

        self.key = key
        self.total = total

        self.__product_uuids: list[str] = []  # 爬到的商品的uuid, 用于在上传成功后 调用 self.clear() 删除本地图片

    def run(self) -> tuple[bool, Union[list[Product], str]]:
        """
        :return: (是否正常完成, 爬取到的数据列表 或 错误信息)
        """
        with ExtraOperation(self.d):
            return self.__run()

    def __run(self) -> tuple[bool, Union[list[Product], str]]:
        self.d.app_stop(APPNAME)
        self.d.app_start(APPNAME)

        try:
            return self.__开始爬取()
        except UiObjectNotFoundError as e:
            return False, f'未找到元素 {e}'

        except XPathElementNotFoundError as e:
            return False, f'未找到元素 {e}'

    def __开始爬取(self) -> tuple[bool, Union[list[Product], str]]:
        success, info = self.__点击主页搜索框输入文字并搜索()
        if not success:
            return False, info

        result: list[Product] = []

        # 不用 while True, 防止某个逻辑不通进入死循环
        for i in range(100):

            # 搜索到的结果界面
            all_search_data_elem = self.d(descriptionContains='¥\n')
            if not all_search_data_elem.wait():
                return False, '未找到-搜索结果'

            for elem in all_search_data_elem:    # todo 这里偶尔找不到
                if len(result) >= self.total:
                    break

                if elem.info['contentDescription'] == '大家都在搜':
                    continue

                elem.click()  # 点击进入商品详情页

                # 有的元素可视范围太小, 可能检测到但点击不到, 这里点击后如果等到超时 右上角订阅按钮 依然存在, 说明没进入详情页, 跳过
                if not self.d(description='订阅').wait_gone():
                    continue

                # 若正常点进去详情页, 去执行爬取的逻辑
                success, data = self.__获取商品详情页的信息()

                if success:
                    result.append(data)

                print(success, data)

                self.d.press('back')  # 退出商品详情页
                time.sleep(2)

            # 爬取的结果够的话直接跳出
            if len(result) >= self.total:
                break

            # 爬取的结果不够的话继续翻页
            # 这里向上翻3次, 每次半屏, 确保不会重复点击
            if swipe_already_end(self.d, lambda: [self.d.swipe(0.5, 0.7, 0.5, 0.2, steps=400) for _ in range(3)]):
                break

            # 滑动到底也能用这种判断, 都加上, 不影响
            if self.d(description='哎呀，到底了').exists:
                break

        return True, result

    def __点击主页搜索框输入文字并搜索(self) -> tuple[bool, str]:
        # 点击主页搜索框
        self.d(resourceId='com.taobao.idlefish:id/title').click()
        # 点击后等待动画过后你输入框出现
        self.d(className='android.widget.EditText').wait()
        # 切换成adb键盘
        self.d.set_input_ime()

        # 部分手机上一步获取到输入框后, 可能会卡顿, 搜索词第一次填不上去 (先尝试几次, 都不行再走正常流程进行 return)
        send_key_to_editor_success = False
        for i in range(3):
            # 输入查询关键字
            if self.d.send_keys(self.key):
                # 再次确认搜索框存在且有输入的自定义关键字
                if self.d(className='android.widget.EditText', textStartsWith=self.key).wait():
                    send_key_to_editor_success = True
                    break

        if not send_key_to_editor_success:
            # 输入查询关键字
            if not self.d.send_keys(self.key):
                return False, '输入关键词失败'

            # 再次确认搜索框存在且有输入的自定义关键字
            if not self.d(className='android.widget.EditText', textStartsWith=self.key).wait():
                return False, '未找到-输入后的搜索框'

        # 点击搜索按钮
        self.d(description='搜索').click()
        return True, ''

    def __获取商品详情页的信息(self) -> tuple[bool, Union[Product, str]]:
        """
        :return: (是否正常返回, 得到的数据 或 错误信息)
        """
        # 点进去后, ui还会变动一次, 可以等待 `商品详情顶部搜索栏`(注意: 不是 `搜索结果界面的搜索栏`) 加载出来 作为 ui变动完成的标识
        # 同时如果点到用户主页, 广告, 首页是视频的情况, 也可以用这个标志检测到
        if not self.d(description='搜索栏').wait():
            return False, '未找到-商品详情顶部搜索栏, 可能是非正常商品界面'

        # 爬取的该条数据的唯一id
        product_uuid = uuid.uuid4().hex

        # 价格
        if not (price_elem := self.d(descriptionMatches=r'.*现价.*¥\n[\w\W]*浏览$')).wait():
            return False, '未找到-价格'

        price = re.findall(r'现价(.*?) , ', price_elem.info['contentDescription'])

        if len(price) == 0:
            return False, '找到了价格元素, 但正则匹配价格时出错'

        price = float(price[0])

        success, desc = get_product_desc(self.d, is_crawl_task=True)
        if not success:
            return False, desc

        # 不断滑动, 直到出现图片
        img_elem = self.d(description='宝贝图片1')  # 物品至少有一个图片, 这里直接用 '宝贝图片1' 作查找关键字

        for i in range(100):
            if img_elem.exists:
                break
            else:
                self.__向下翻页()

            if i == 99:
                return False, '未找到 宝贝图片1'

        # 这两个按纽 不定出现
        buy_now_elem = self.d(description='立即购买')  # 立即购买 按钮
        i_want_elem = self.d(description='我想要')  # 我想要 按钮

        if buy_now_elem.exists:
            anchors_btn = buy_now_elem
        elif i_want_elem.exists:
            anchors_btn = i_want_elem
        else:
            return False, '未找到-立即购买按钮-或-我想要按钮'

        # 图片出现后, 接着滑动, 使图片下边界高于按钮, 这样才能点击放大
        while not img_elem.bounds()[3] < anchors_btn.bounds()[1]:
            self.__向下翻页()

        # 点击进入图片放大预览
        img_elem.click()

        # 左下角的计数控件
        counter_elem = self.d(descriptionContains='1/')
        if not counter_elem.wait():
            return False, '未找到-计数控件'

        # 获取图片总数, 判断左滑几次
        img_num = int(counter_elem.info['contentDescription'][-1])

        local_img_path: list[Path] = []
        os.makedirs(IMG_PATH / product_uuid)
        self.__product_uuids.append(product_uuid)
        for i in range(img_num):
            # 截图
            img = self.d.screenshot(format='opencv')

            # todo 用ocr识别图片是否有水印文字, 有就直接跳过这个商品

            # 截取有效图片
            up_edge, down_edge = self.__获取图片上下边界(img)
            img_clip = img[up_edge:down_edge]

            img_path = IMG_PATH / product_uuid / f'{i}.jpg'
            cv2.imwrite(img_path, img_clip)
            local_img_path.append(img_path)

            # 左滑并等待几秒让图片滑动动画结束
            self.d.swipe(0.8, 0.5, 0, 0.5, steps=20)
            time.sleep(1)

        # 退出图片放大预览
        self.d.press('back')
        time.sleep(2)

        return True, Product(
            product_uuid=product_uuid,
            price=price,
            desc=desc,
            local_img_path=local_img_path
        )

    def __获取图片上下边界(self, img: np.ndarray) -> tuple[int, int]:
        """
        点开图片后, 调用该函数返回目标区域的上下边界

        :param img: 原始截屏图片

        :return: 目标图片的上下边界
        """

        # 安卓系统顶部状态栏的下边界
        status_bar_down_edge = self.d(resourceId='com.android.systemui:id/status_bar_container').bounds()[3]

        # 闲鱼 查看原图 按钮的上边界
        show_raw_up_edge = self.d(description='查看原图').bounds()[1]

        # ############################## 截图要在上面两个边界中间截, 才不会截取到图片以外的信息

        img = img[status_bar_down_edge:show_raw_up_edge, :]  # 先进行一次截取, 方便后续处理
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        height, width = img_gray.shape

        target_up_edge = 0
        target_down_edge = height

        for i in range(1, height):
            # 若 第 i-1 行 全是黑色 且 第 i 行 有非黑色的像素
            if np.all(img_gray[i - 1:i] == 0) and np.any(img_gray[i] != 0):
                target_up_edge = i
                break

        for i in range(target_up_edge, height - 1):
            # 若 第 i 行 有非黑色的像素 且 第 i+1 行 全是黑色
            if np.any(img_gray[i] != 0) and np.all(img_gray[i + 1] == 0):
                target_down_edge = i + 1
                break

        # 函数开始时进行了一次裁剪返回时需要加上安卓系统状态栏高度作为偏移量
        return target_up_edge + status_bar_down_edge, target_down_edge + status_bar_down_edge

    def __向下翻页(self):
        """
        界面从下向上滚动, 经测试能很稳定的滑动 1/10 屏距离
        """
        self.d.swipe(0.5, 0.5, 0.5, 0.40, steps=100)

    def clear(self):
        """
        清除此次任务留下的图片
        """
        for i in self.__product_uuids:
            shutil.rmtree(IMG_PATH / i)


if __name__ == '__main__':
    device = uiautomator2.connect('192.168.31.69:5555')
    device.settings['wait_timeout'] = 10.0  # 测试, 将超时时间设个小值, 方便快速调试, 原值是 20.0
    c = Crawl(device, 'iphone', 2)
    print(c.run())
    c.clear()
