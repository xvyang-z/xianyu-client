# import re
# import time
# from typing import Union
#
# import uiautomator2
# from scripts.common.click_my_mypublish_page_search_edit_and_input import click_my_mypublish_page_search_edit_and_input
# from scripts.common.extra_operation import ExtraOperation
# from scripts.common.get_product_desc import get_product_desc
# from settings import APPNAME
# from uiautomator2 import Device, UiObject
# from uiautomator2.exceptions import UiObjectNotFoundError, XPathElementNotFoundError
#
#
# class Promotion:
#     def __init__(self, d: Device, desc: str, price: float, number: str = '100-125'):
#         """
#         :param d: 设备实例
#         :param desc: 商品描述
#         :param price: 商品价格
#         :param number: 推广人数
#         """
#
#         self.d = d
#         self.desc = desc
#         self.price = price
#         self.number = number
#
#     def run(self) -> tuple[bool, Union[float, str]]:
#         """
#         开始执行闲鱼币换曝光
#         """
#         with ExtraOperation(self.d):
#             return self.__run()
#
#     def __run(self) -> tuple[bool, str]:
#         self.d.app_stop(APPNAME)
#         self.d.app_start(APPNAME)
#
#         try:
#             return self.__开始加曝光()
#         except UiObjectNotFoundError as e:
#             return False, f'未找到元素 {e}'
#
#         except XPathElementNotFoundError as e:
#             return False, f'未找到元素 {e}'
#
#     def __开始加曝光(self) -> tuple[bool, Union[float, str]]:
#         self.d.xpath('//*[@text="我的"]').parent().click()
#
#         self.d(descriptionStartsWith='我发布的').click()
#
#         success, search_elem = click_my_mypublish_page_search_edit_and_input(self.d, self.desc)  # 根据商品描述进行搜索
#         if not success:
#             search_elem: str
#             return False, search_elem
#
#         search_elem: Union[UiObject, list[UiObject]]
#
#         all_search_data_elem = self.d(descriptionStartsWith='更多')
#
#         if not all_search_data_elem.wait():
#             return False, '未找到-搜索结果'
#         for elem in all_search_data_elem:
#             elem.click()
#             price_elem = self.d(descriptionMatches=r'.*现价.*¥\n[\w\W]*浏览$')
#             price = re.findall(r'现价(.*?) , ', price_elem.info['contentDescription'])
#             if len(price) == 0:
#                 self.d.press('back')
#                 continue
#             price = float(price[0])
#             success, desc = get_product_desc(self.d, is_crawl_task=True)
#             if not success:
#                 self.d.press('back')
#                 continue
#
#                 # 在发布时可能会在最后加上个 `\n感兴趣的话点"我想要"和我私聊吧~`, 用 startswith 比较
#             if not desc.startswith(self.desc) or price != self.price:  # 判断以这个desc开头
#                 self.d.press('back')
#                 continue
#
#             self.d(description='管理').wait()
#             self.d(description='管理').click()
#             self.d(description='推广宝贝').wait()
#             self.d(description='推广宝贝').click()
#             self.d(text=self.number).wait()
#             time.sleep(1)
#             self.d(text=self.number).click()
#             if self.d(text='去赚币'):
#                 return False, '当前余额不足，赚点币再来吧'
#             else:
#                 self.d(text='开始推广').click()
#                 return True, ''
#         return False, '未找到符合描述和价格的商品'
#
#
# if __name__ == '__main__':
#     device = uiautomator2.connect('192.168.1.214:5555')
#     device.settings['wait_timeout'] = 10.0  # 测试, 将超时时间设个小值, 方便快速调试, 原值是 20.0
#
#     rp = ReducePrice(
#         d=device,
#         desc='React+Node开发接单',
#         price=666,
#         number='100-125',
#     )
#
#     print(rp.run())
#
