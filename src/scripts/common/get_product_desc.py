import uiautomator2
from scripts.common.find_most_like_elem import find_most_like_elem
from scripts.elem_img import TemplatePath
from uiautomator2 import Device


def get_product_desc(d: Device, is_crawl_task=False) -> tuple[bool, str]:
    """
    通过全选复制, 获取商品描述

    :param d: 设备实例
    :param is_crawl_task: 是否是爬取任务调用这个函数.
        如果爬别人的商品, 闲鱼交易须知中是 '买前了解退货规则'
        其他脚本管理自己号上的商品, 是 '卖前了解退货规则'
    """
    if not d(description='搜索栏').wait():
        return False, '未找到-商品详情顶部搜索栏'

    scroll_elem = d.xpath('//android.widget.ScrollView[@index=0]')

    # 描述元素 (使用 剪贴板 功能 进行获取)
    # 如果没有像 闲鱼交易须知, 验货宝, 降价信息这些元素 的话, 描述元素应在 scroll_elem 下 index = 2 的位置上
    desc_elem_index = 2

    # 话题标签, 多个标签也只加1
    screen_shot = d.screenshot()
    label_tags = [
        TemplatePath.话题标签1,
        TemplatePath.话题标签2,
        TemplatePath.话题标签3,
    ]
    for tag in label_tags:
        ok, _ = find_most_like_elem(screen_shot, tag)
        if ok:
            desc_elem_index += 1
            break

    # 芝麻工作证
    ok, _ = find_most_like_elem(screen_shot, TemplatePath.芝麻工作证)
    if ok:
        desc_elem_index += 1

    # 验号担保
    if d(description=r'下单后由专业服务商验号，先验后买更安心').exists:
        desc_elem_index += 1

    # 自己发的商品有时候会被审核
    if d(descriptionMatches=r'^宝贝审核中...\n.*?审核通过后自动上架$').exists:
        desc_elem_index += 1

    # 公益宝贝
    if d(descriptionStartsWith=r'交易成功后将捐赠').exists:
        desc_elem_index += 1

    # 可选的类别信息
    if d(descriptionMatches=r'.* 可选$').exists:
        desc_elem_index += 1

    # 描述不符全额退
    if d(description='24小时发货 · 描述不符全额退').exists:
        desc_elem_index += 1

    # 描述不符全额退
    if d(description='描述不符全额退\n满足条件时，买家可申请全额退款').exists:
        desc_elem_index += 1

    # 降价信息
    if d(descriptionStartsWith='累计降价').exists:
        desc_elem_index += 1

    if d(descriptionMatches='近.*?天降价.*?').exists:
        desc_elem_index += 1

    # 购入价??折
    if d(descriptionStartsWith='购入价').exists:
        desc_elem_index += 1

    # 卖家不支持砍价
    if d(description='卖家不支持砍价\n价格已最低，多聊聊宝贝细节吧~').exists:
        desc_elem_index += 1

    # 卖家支持小刀
    if d(description='卖家支持小刀\n刀成功可获优惠，快和卖家聊聊吧～').exists:
        desc_elem_index += 1

    # 闲鱼交易须知
    __text = ('买' if is_crawl_task else '卖') + '前了解退货规则，保障你的交易权益'
    if d(description=__text).exists:
        desc_elem_index += 1

    # 已验货
    if d(description='已验货\n卖家已缴纳保证金并出具报告').exists:
        desc_elem_index += 1

    # 严选
    if d(description='宝贝已验货并寄存于验货仓，下单直发').exists:
        desc_elem_index += 1

    # 验货宝
    if d(description='下单后寄至验货中心先验后买，80项专业检测\n本宝贝只走验货宝').exists:
        desc_elem_index += 1

    # 7天无理由退货
    if d(description='7天无理由退货\n承诺买家可申请退货，运费需买家承担').exists:
        desc_elem_index += 1

    # 超时赔付
    if d(descriptionStartsWith='24小时发货\n承诺按时发货，超时将赔付').exists:
        desc_elem_index += 1

    # 描述不符包邮退
    # 还有一种是这样的: `描述不符包邮退\n满足条件时，买家可退货且运费由卖家承担` 一般作为 闲鱼交易须知 的子项出现, 不影响判断位置
    # 还有一种是这样的: `24小时发货 · 描述不符包邮退 · 7天无理由退货`         一般作为 已验货      的子项出现, 不影响判断位置
    if d(description='描述不符包邮退 · 7天无理由退货').exists:
        desc_elem_index += 1

    # 描述元素
    desc_elem = scroll_elem.child(f'/*[@index={desc_elem_index}]')

    if not desc_elem.wait():
        return False, '未找到-描述'

    # 这里需要先切换成 adb 键盘
    d.set_input_ime()

    # 长按呼出全选复制按钮 (先尝试几次, 都不行再走正常流程进行 return)
    copy_successful = False
    for i in range(3):
        desc_elem.long_click()

        if d(description='全选').wait(timeout=2):
            d(description='全选').click()

            if d(description='复制').wait(timeout=2):
                d(description='复制').click()
                copy_successful = True
                break

    if not copy_successful:
        desc_elem.long_click()

        if not d(description='全选').wait():
            return False, '未找到-全选'

        d(description='全选').click()

        if not d(description='复制').wait():
            return False, '未找到-复制'

        d(description='复制').click()

    return True, d.clipboard


if __name__ == '__main__':
    ddd = uiautomator2.connect('192.168.31.87:5555')
    ddd.settings['wait_timeout'] = 5
    print(get_product_desc(ddd, is_crawl_task=True))
