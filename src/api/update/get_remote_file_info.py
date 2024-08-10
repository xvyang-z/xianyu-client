from typing import Union

import requests
from pydantic import BaseModel

from api import BaseResp


from settings import CLIENT_API, API_HEADER


class FileInfo(BaseModel):
    file: str  # 文件路径, 相对于运行入口
    md5: str   # 文件的md5信息
    size: int  # 大小, 单位 byte


class Data(BaseModel):
    update_info: str
    file_info: list[FileInfo]


class Resp(BaseResp[Union[Data]]):
    ...


def get_remote_file_info() -> tuple[bool, Data | str]:
    url = CLIENT_API + '/get_remote_file_info'

    try:
        resp = requests.get(
            url,
            headers=API_HEADER,
        )
        resp = Resp(**resp.json())
    except Exception as e:
        return False, str(e)

    if resp.code == 0:
        return True, resp.data
    else:
        return False, resp.message
