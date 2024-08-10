import time
from typing import Union, Iterable

from uiautomator2 import Device, UiObject

import jieba
import re
from collections import Counter


def __get_most_word(word: str) -> str:
    """
    获取出现次数最多的词作为搜索关键字
    """
    # 闲鱼是用前30个字符进行分词做查找索引的, 使用30个字符后的词查不到, 这里将分词的范围也限制到前30个字符
    word = word[:30]

    # 仅保留: 中文 英文 空格
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z ]', '', word)
    # 使用 jieba 进行分词
    words = jieba.lcut(text)
    # 去除单字的词
    words = [word for word in words if len(word) > 1]

    # 使用 Counter 来统计每个词的出现频率
    word_counts = Counter(words)
    # 找到出现频率最高的词及其次数
    most_word, freq = word_counts.most_common(1)[0]

    return most_word


def click_my_mypublish_page_search_edit_and_input(
        d: Device,
        desc: str
) -> tuple[bool, Union[str, Union[UiObject, Iterable[UiObject]]]]:
    """
    点击 我的 - 我发布的 - 界面的- 搜索按钮 - 输入关键词

    :param d: 设备实例
    :param desc: 商品的描述
    """

    # 先点击搜索按钮

    # 在卖按钮的父元素(是个包含三个按钮的盒子)
    select_box_elem = d.xpath('//*[@content-desc="第 1 个标签，共 3 个"]').parent()
    # 在卖按钮的父元素索引
    select_box_elem_index = select_box_elem.info['index']

    # 搜索元素向后偏移 1
    search_elem_index = select_box_elem_index + 1

    # 如果存在加入卖场的按钮再偏移 1
    if d(description='加入卖场').exists:
        search_elem_index += 1
    # 如果是开通鱼小铺,则会显示一个图标和一个宝贝工具，两者独立存在，按钮再偏移+2
    if d(description='宝贝工具').exists:
        search_elem_index += 2

    time.sleep(1)
    # 点击 `搜索按钮` (放大镜图标)
    d.xpath(f'//android.widget.ScrollView[@index=0]/*[@index="{search_elem_index}"]').click()

    # 点击搜索框并搜索指定的描述关键字
    # 左上角`返回按钮`的中心 x, y 坐标
    d(textStartsWith='搜索你在卖的宝贝').child()[0].wait()
    back_center_x, back_center_y = d(textStartsWith='搜索你在卖的宝贝').child()[0].center()

    # 点击同高位置的屏幕中心, 聚焦搜索框
    d.click(d.info['displayWidth'] // 2, back_center_y)

    # 先切换键盘
    d.set_input_ime()

    # 部分手机上一步点击输入框后, 可能会卡顿, 搜索词第一次填不上去 (先尝试几次, 都不行再走正常流程进行 return)
    send_key_to_editor_success = False
    search_key = __get_most_word(desc)
    for i in range(3):
        # 输入查询关键字
        if d.send_keys(search_key):
            # 再次确认搜索框存在且有输入的自定义关键字
            if d(className='android.widget.EditText', textStartsWith=search_key).wait(timeout=2):
                send_key_to_editor_success = True
                break

    if not send_key_to_editor_success:
        # 输入查询关键字
        if not d.send_keys(search_key):
            return False, '输入关键词失败'

        # 再次确认搜索框存在且有输入的自定义关键字
        if not d(className='android.widget.EditText', textStartsWith=search_key).wait():
            return False, '未找到-输入后的搜索框'

    # 点击 enter 搜索
    d.press('enter')

    search_elem: Union[UiObject, Iterable[UiObject]] = d(descriptionMatches=r'^更多\n(降价\n)?编辑\n[\w\W]*')

    # 如果等到超时还没有搜索出结果
    if not search_elem.wait():
        if d(description='小闲鱼没有找到相关宝贝~').exists:
            return False, '在已发布的商品中未搜索到相关描述的商品'
        else:
            return False, '搜索后出现意外情况, 需要更改脚本'

    # 如果出现搜索结果, 筛选下搜索结果, 确保元素整体可视, 不能被系统导航键 或 无法点击的区域覆盖
    # 系统是 经典导航键导航: 最后一个元素要高于 home 键上边界: resourceId=com.android.systemui:id/home
    # 系统是 全面屏手势导航: 最后一个元素要高于 屏幕高度 - 100px

    if (home_btn := d(resourceId='com.android.systemui:id/home')).exists:
        height_edge = home_btn.bounds()[1]
    else:
        height_edge = d.info['displayHeight'] - 100

    search_elem = [elem for elem in search_elem if elem.bounds()[3] <= height_edge]

    return True, search_elem
