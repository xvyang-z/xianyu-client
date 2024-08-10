# import time
#
# import uiautomator2
# from scripts.common.extra_operation import ExtraOperation
# from scripts.common.swipe_util import swipe_already_end
# from settings import APPNAME
# from uiautomator2 import Device
# from uiautomator2.exceptions import XPathElementNotFoundError, UiObjectNotFoundError
#
#
# class AutoReply:
#     def __init__(self, d: Device):
#         self.d = d
#
#     def run(self) -> tuple[bool, str]:
#         with ExtraOperation(self.d):
#             return self.__run()
#
#     def __run(self) -> tuple[bool, str]:
#         self.d.app_stop(APPNAME)
#         self.d.app_start(APPNAME)
#
#         try:
#             return self.__开始自动回复()
#         except UiObjectNotFoundError as e:
#             return False, f'未找到元素 {e}'
#
#         except XPathElementNotFoundError as e:
#             return False, f'未找到元素 {e}'
#
#     def __开始自动回复(self) -> tuple[bool, str]:
#         self.d.xpath('//*[@text="消息"]').parent().click()
#
#         # 闲鱼网络超时设置为 2s, 2秒内从服务器获取不到数据会显示本地离线数据
#         # 这里直接等待 4s 后开始进行操作 (给动画加载时长留余)
#         time.sleep(4)
#
#         while True:
#             all_no_read_elem = self.d.xpath("//*[starts-with(@content-desc, '未读数')]").all()
#
#             # 遍历每一条未读消息
#             for no_read_elem in all_no_read_elem:
#                 # 未读消息后一个元素是标题, 可以通过这个过滤系统消息, 也可以用于后续报错提示
#                 title_index = no_read_elem.info['index']
#                 title_elem = self.d.xpath(no_read_elem.parent().get_xpath() + f'/*[@index={title_index + 1}]').get()
#                 title: str = title_elem.info['contentDescription']
#
#                 if title in ['通知消息', '互动消息']:
#                     continue
#
#                 no_read_elem.click()
#
#                 success, msg = self.__获取未读消息()
#                 if not success:
#                     return False, msg
#
#                 success, reply = self.__调接口获取智能回复(msg)
#                 if not success:
#                     return False, msg
#
#                 success, result = self.__发送智能回复(reply)
#                 if not success:
#                     return False, result
#
#                 # 这里需要点击返回两次, 第一次收起键盘, 第二次才是返回上一页
#                 self.d.press('back')
#                 time.sleep(1)
#                 self.d.press('back')
#                 time.sleep(1)
#
#             if swipe_already_end(self.d, lambda: self.d.swipe(0.5, 0.7, 0.5, 0.2, steps=200)):
#                 break
#
#         return True, ''
#
#     def __获取未读消息(self) -> tuple[bool, str]:
#         self.d.xpath("//*[@content-desc='头像']").wait()
#         all_avatar = self.d.xpath("//*[@content-desc='头像']").all()
#
#         # 逆序遍历 显示在当前屏幕 的 聊天记录
#         # 通过 头像位置 < 屏幕宽度一半 判断是对方的头像, 大于则是自己的头像
#         # 取 自己最后一条消息 后的 对方消息
#         all_msg = []
#
#         for avatar_elem in all_avatar[::-1]:
#             avatar_elem_center_x = avatar_elem.center()[0]
#             screen_center_x = int(self.d.info['displayWidth'] / 2)
#
#             # 如果是对方的消息行
#             if avatar_elem_center_x < screen_center_x:
#
#                 # 通过对方头像元素先获取到父元素, 再拿这个父元素下所有 android.view.View 的消息内容
#                 msg_elem = self.d.xpath(avatar_elem.parent().get_xpath() + '/android.view.View').all()
#                 msg: list[str] = [i.info['contentDescription'] for i in msg_elem]
#                 all_msg.extend(msg)
#
#             else:
#                 break
#
#         # 上面是倒序, 这里再调整为正常顺序
#         all_msg.reverse()
#
#         result = '\n'.join(all_msg)
#
#         if result == '':
#             return False, '有未读消息但未获取到'
#         else:
#             return True, result
#
#     def __调接口获取智能回复(self, msg: str) -> tuple[bool, str]:
#         # todo 接口生成, 生成回答时, 带不带商品描述?
#         answer = '在的'
#         return True, answer
#
#     def __发送智能回复(self, reply: str) -> tuple[bool, str]:
#         self.d.set_input_ime()
#         self.d(description='想跟TA说点什么...').click()
#
#         time.sleep(2)  # 点击后稍等下, 否则文字可能输入不上去
#
#         self.d.send_keys(reply)
#
#         self.d(description='发送').click()  # 输入框有值才会出现这个按钮
#
#         self.d(description='发送').wait_gone()  # 发送成功这个按钮会消失
#
#         return True, ''
#
#
# if __name__ == '__main__':
#     d1 = uiautomator2.connect('192.168.1.169:5555')
#     print(
#         AutoReply(d1).run()
#     )
