import json
from dataclasses import dataclass, asdict

from settings import USER_CONFIG_FILE


@dataclass
class UserConfig:
    """
    用户在运行时产生的配置, 每次更改都会写到硬盘
    """

    token: str = ''

    def __init__(self):
        self.__is_init = True
        self.__load()
        self.__is_init = False

    def __load(self):
        if not USER_CONFIG_FILE.exists():
            self.__save()
        else:
            with open(USER_CONFIG_FILE, 'r', encoding='utf-8') as config_file:
                json_data = json.load(config_file)

            for name, value in json_data.items():
                setattr(self, name, value)

    def __save(self):
        with open(USER_CONFIG_FILE, 'w', encoding='utf-8') as config_file:
            json.dump(asdict(self), config_file)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if not self.__is_init:
            self.__save()


user_config = UserConfig()
