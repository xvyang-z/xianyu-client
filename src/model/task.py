import json
from enum import Enum
from typing import Callable
from uiautomator2 import Device


class Cmd(Enum):
    爬取商品 = '爬取商品'
    发布商品 = '发布商品'
    删除商品 = '删除商品'
    下架商品 = '下架商品'
    重新上架 = '重新上架'
    商品降价 = '商品降价'
    开启闲鱼币抵扣 = '开启闲鱼币抵扣'
    一键擦亮 = '一键擦亮'
    签到闲鱼币 = '签到闲鱼币'

    @property
    def handle_func(self) -> Callable[[Device, 'Task'], None]:
        """
        获取 枚举 对应的 handle 函数
        """
        from handle.handle_crawl import handle_crawl
        from handle.handle_delist import handle_delist
        from handle.handle_publish import handle_publish
        from handle.handle_delete import handle_delete
        from handle.handle_open_fish_currency_deduction import handle_open_fish_currency_deduction
        from handle.handle_republish import handle_republish
        from handle.handle_reduce_price import handle_reduce_price
        from handle.handle_polish import handle_polish
        from handle.handle_get_coin_and_signin import handle_get_coin_and_signin

        return {
            Cmd.爬取商品: handle_crawl,
            Cmd.发布商品: handle_publish,
            Cmd.删除商品: handle_delete,
            Cmd.下架商品: handle_delist,
            Cmd.重新上架: handle_republish,
            Cmd.商品降价: handle_reduce_price,
            Cmd.开启闲鱼币抵扣: handle_open_fish_currency_deduction,
            Cmd.一键擦亮: handle_polish,
            Cmd.签到闲鱼币: handle_get_coin_and_signin,
        }[self]

    @property
    def success_route(self) -> str:
        """
        获取 枚举 对应的 执行成功的路由
        """
        return {
            Cmd.爬取商品: '/success/crawl',
            Cmd.发布商品: '/success/publish',
            Cmd.删除商品: '/success/delete',
            Cmd.下架商品: '/success/delist',
            Cmd.重新上架: '/success/republish',
            Cmd.商品降价: '/success/reduce_price',
            Cmd.开启闲鱼币抵扣: '/success/open_fish_currency_deduction',
            Cmd.一键擦亮: '/success/polish',
            Cmd.签到闲鱼币: '/success/get_coin_and_signin'
        }[self]

    @staticmethod
    def from_str(s: str) -> 'Cmd':
        """
        从字符串获取对应的枚举变量
        """
        return Cmd[s]


class Task:

    def __init__(self, task_id: int, cmd: 'Cmd', cmd_args: dict, device_flag: str, device_name: str, is_open_fish_shop: bool):
        self.task_id = task_id

        self.cmd = cmd
        self.cmd_args = cmd_args

        self.device_flag = device_flag
        self.device_name = device_name
        self.is_open_fish_shop = is_open_fish_shop

    def to_json_str(self) -> str:
        return json.dumps({
            'task_id': self.task_id,
            'cmd': self.cmd,
            'cmd_args': self.cmd_args,
            'device_flag': self.device_flag,
            'device_name': self.device_name,
            'is_open_fish_shop': self.is_open_fish_shop
        })

    @staticmethod
    def from_json_str(json_str: str) -> 'Task':
        dic = json.loads(json_str)
        return Task(**dic)
