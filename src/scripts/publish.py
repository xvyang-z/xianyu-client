import json
import shutil
import time

import requests
import uiautomator2
from uiautomator2 import Device
from uiautomator2.exceptions import UiObjectNotFoundError, XPathElementNotFoundError

from scripts.common.extra_operation import ExtraOperation
from scripts.common.find_most_like_elem import find_most_like_elem
from scripts.common.swipe_util import swipe_until_find_elem
from scripts.elem_img import TemplatePath
from settings import APPNAME, DOWNLOAD_PATH, SERVER_HOST


class Publish:
    def __init__(self, d: Device, uuid: str, price: float, desc: str, images: list[str], location: list[str]):
        """
        :param d: 设备实例
        :param uuid: 要发布商品的 uuid
        :param price: 要发布商品的价格
        :param desc: 要发布商品的描述
        :param images: 要发布商品的图片的路由
        :param location: 要发布商品的所在地
        """
        self.d = d

        self.uuid = uuid
        self.price = price
        self.desc = desc
        self.images = images
        self.location = location

    def run(self) -> tuple[bool, str]:
        """
        开始执行发布任务
        """
        with ExtraOperation(self.d):
            return self.__run()

    def __run(self) -> tuple[bool, str]:
        self.d.app_stop(APPNAME)
        self.d.app_start(APPNAME)

        # 先从服务器下载图片并推送到对应设备上
        success, info = self.__从服务器下载图片并推到设备上()
        if not success:
            return False, info

        try:
            with self.d.watch_context() as ctx:
                ctx.when('//*[@content-desc="你有未编辑完成的宝贝，是否继续？"]').when('//*[@content-desc="放弃"]').click()
                return self.__开始发布()
        except UiObjectNotFoundError as e:
            return False, f'未找到元素 {e}'

        except XPathElementNotFoundError as e:
            return False, f'未找到元素 {e}'

    def __开始发布(self) -> tuple[bool, str]:
        # 点击底部的 卖闲置
        self.d.xpath('//*[@resource-id="com.taobao.idlefish:id/indicator_itmes"]/*[@index=2]').click()

        self.d(descriptionContains='发闲置').click()

        # todo 一个账号发满 50/500 个, 给出提示

        # ### 如果先输入文字和添加图片太多的话, 还要向下翻页才能点击设置价格, 这里先设置 位置, 价格, 再添加图片, 最后输入描述

        self.d(descriptionContains='价格设置').wait()

        # 开通了鱼小铺的账号, 这里有 3 个选项(商品规格, 价格设置, 发货方式), 价格设置在中间, 直接点击中心坐标
        if self.d(description='商品规格\n非必填，设置多个颜色、尺码等').exists:
            self.d(descriptionContains='价格设置').click()
        else:
            # 未开通鱼小铺这里有 2 个选项(价格设置, 发货方式), 价格设置在第 1 个, 使用偏移量, 点击 1/10 高度的坐标
            self.d(descriptionContains='价格设置').click(offset=(0.5, 0.1))

        # 设置价格
        price = str(self.price)
        for i in price:
            self.d(description=i).click()

        # 对开通了鱼小铺的账号进行库存设置, 允许值最大为 10000
        if self.d(description='库存设置').exists:
            self.d(descriptionContains='库存设置').click()
            inventory = "10000"
            for i in inventory:
                self.d(description=i).click()

        self.d(description='确定').click()

        # 点击确定后收回输入键盘有个动画效果, 下一步设置位置需要截图识别, 太快的话可能截不到, 这里等两秒再继续
        time.sleep(2)

        if self.location:
            province, city, county = self.location
            success, info = self.__设置地区(province, city, county)
            if not success:
                return False, info

        # 设置图片
        self.d(description='添加图片').click()
        self.d(description='相册\nTab 1 of 3').click()
        self.d(description='所有文件').click()
        self.d(descriptionContains=self.uuid).click()

        # 选择相册后, 动画稍长, 这里等两秒稳定了再点击
        time.sleep(2)

        for i in self.d.xpath('//*[@content-desc="选择"]').all():
            i.click()

        self.d(descriptionContains='下一步').click()

        #  如果图片过多, 点击下一步会加载一会儿, 此时点击完成会提示, 而不会跳到下一页, 这里等待几秒
        time.sleep(5)

        self.d(description='完成').click()

        self.d.set_input_ime()  # 先切换 adb 键盘
        self.d(description='描述, 描述一下宝贝的品牌型号、货品来源…').click()
        self.d.send_keys(self.desc)

        # 输入完描述后闲鱼会自动添加分类, 没有分类发不出去
        flag_elem = self.d(descriptionMatches=r'^分类.*?')
        if not flag_elem.wait():
            return False, '获取分类信息失败, 无法发布'

        self.d(description='发布').click()

        # 点击发布后等待出现(再发一件 或 发布成功), 才算真正完成任务
        if not (
                self.d(description='发布成功').wait()
                or self.d(description='管理').wait()
                or self.d(description='再发一件').wait()
        ):
            return False, '点击 发布按钮 后 等待 发布成功的标志 超时'

        return True, ''

    def __从服务器下载图片并推到设备上(self) -> tuple[bool, str]:
        """
        下载图片并推送到设备上
        """
        # 先从服务器下载所有图片
        local_img_path = []
        for img in self.images:
            url = SERVER_HOST + img

            try:
                resp = requests.get(url)
            except Exception as e:
                return False, f'下载图片时出错 {e}'

            img_path = DOWNLOAD_PATH / self.uuid / img.split('/')[-1]

            if not img_path.parent.exists():
                img_path.parent.mkdir()

            with open(img_path, 'wb') as f:
                f.write(resp.content)

            local_img_path.append(img_path)

        # 将下载下来的图片推到对应设备上的相册文件夹, 不同手机相册文件夹可能不同, 这里使用小米手机
        for img_path in local_img_path:
            self.d.push(img_path, f'/storage/emulated/0/DCIM/{self.uuid}/{img_path.name}')

        # 广播刷新图片文件夹, 让app能察觉到这个文件夹
        self.d.shell('am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///storage/emulated/0/DCIM')

        return True, ''

    def clear(self):
        """
        清除此次任务留下的图片
        """
        shutil.rmtree(DOWNLOAD_PATH / self.uuid)
        self.d.shell(f'rm -rf /storage/emulated/0/DCIM/{self.uuid}')
        # 广播刷新图片文件夹, 避免刷新到这个文件夹
        self.d.shell('am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///storage/emulated/0/DCIM')

    def __设置地区(self, province: str, city: str, county: str) -> tuple[bool, str]:
        success, elem_info = find_most_like_elem(self.d.screenshot(), template_path=TemplatePath.选择位置的图标)
        if not success:
            return False, '未找到选择位置的图标'

        self.d.click(*elem_info.center)

        # 点击位置后, 会加载附近位置, 还有个动画效果, 这里等加载出来再去滑动
        self.d(description='附近地址').wait()

        time.sleep(2)

        self.d(scrollable=True).scroll.toEnd()

        # 滑动到最后有个弹簧效果, 等两秒再进行下一步操作
        time.sleep(2)

        self.d(description='更多其他区域').click(offset=(0.1, 0.5))

        province_elem = self.d(text=province)
        if not swipe_until_find_elem(self.d, province_elem, lambda: self.d.swipe(0.5, 0.5, 0.5, 0.25, steps=100)):
            return False, f'未找到一级地区 {province}'

        province_elem.click()
        time.sleep(1)  # 点击后等待一秒, 否则滑动可能不生效

        # 当进入第二级地区时, 当二级太多时, 这个界面初始状态下会向下偏移一屏, 这里先滑到顶部
        self.d.swipe(.5, .25, .5, .75, steps=20)
        self.d.swipe(.5, .25, .5, .75, steps=20)
        time.sleep(1)

        city_elem = self.d(text=city)
        if not swipe_until_find_elem(self.d, city_elem, lambda: self.d.swipe(0.5, 0.5, 0.5, 0.25, steps=100)):
            return False, f'未找到二级地区 {city}'

        city_elem.click()

        county_elem = self.d(text=county)
        if not swipe_until_find_elem(self.d, county_elem, lambda: self.d.swipe(0.5, 0.5, 0.5, 0.25, steps=100)):
            return False, f'未找到三级地区 {county}'

        county_elem.click()

        # 点击三级地区后会自动跳转到发布页, 此时发布页的位置会显示 后两级地区的名字, 用一个空格隔开, 这时每个字符后还会追加一个 零宽字符
        time.sleep(2)
        flag_text = f'{city} {county}'
        if not self.d(description=''.join([i + '​' for i in flag_text])).exists:
            return False, '点击三级地区后发布界面未找到选择的地区'

        return True, ''


if __name__ == '__main__':
    device = uiautomator2.connect('192.168.1.169:5555')
    device.settings['wait_timeout'] = 10.0  # 测试, 将超时时间设个小值, 方便快速调试, 原值是 20.0

    cmd_args = json.loads(
        "{\"uuid\": \"90c45812a445476497cfd73b5bb51be5\", \"price\": 80.0, \"desc\": \"\\u6c38\\u4e45\\u724c\\u6298\\u53e0\\u81ea\\u884c\\u8f66\\uff0c\\u5f88\\u597d\\u9a91\\u4e5f\\u5e26\\u51cf\\u9707\\u7684\\u90a3\\u79cd\\uff0c\\u4e0d\\u98a0\\u7c38\\u7684\\u3002\\n\\u611f\\u5174\\u8da3\\u7684\\u8bdd\\u70b9\\u201c\\u6211\\u60f3\\u8981\\u201d\\u548c\\u6211\\u79c1\\u804a\\u5427\\uff5e\", \"images\": [\"/uploads/user/1/product_img/90c45812a445476497cfd73b5bb51be5/7c287eb18c514c44ac172ced9db9e676.jpg\", \"/uploads/user/1/product_img/90c45812a445476497cfd73b5bb51be5/3b886a3b39a44b7ea33c1302c466ab5f.jpg\", \"/uploads/user/1/product_img/90c45812a445476497cfd73b5bb51be5/f8a5b3dc1c8a463ab4fcbfdb2b179e20.jpg\", \"/uploads/user/1/product_img/90c45812a445476497cfd73b5bb51be5/c5ed239b3e1e4a08b16e25d757d4cce2.jpg\", \"/uploads/user/1/product_img/90c45812a445476497cfd73b5bb51be5/801b9b348971438db7058a3f781aebb9.jpg\", \"/uploads/user/1/product_img/90c45812a445476497cfd73b5bb51be5/420291aedd60487a9850e42b6934b3ab.jpg\"]}")

    p = Publish(
        d=device,
        uuid="30dcc9cff0a84f589fae5a8015105364",
        price=580.0,
        desc="网页开发维护、小程序开发维护、App定制开发维护， html，css， js，vue，Python，php，iOS，安卓等，可提供源码。\n数据爬取等\n\n专业团队，价格便宜，欢迎老板咨询",
        images=[
            "/uploads/user/1/product_img/30dcc9cff0a84f589fae5a8015105364/e9e08064dde049bd8995de7f1ac5c0cf.jpg",
            "/uploads/user/1/product_img/30dcc9cff0a84f589fae5a8015105364/e2117f34684b406d8f69d9a7f6fa0b88.png"
        ],
        location=[]
    )

    print(p.run())

    p.clear()

