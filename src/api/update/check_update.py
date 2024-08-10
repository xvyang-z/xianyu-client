import requests
from pydantic import BaseModel

from api import BaseResp

from settings import CLIENT_API, API_HEADER


class Data(BaseModel):
    version: str


class Resp(BaseResp[Data]):
    ...


def check_update() -> tuple[bool, Data | str]:
    url = CLIENT_API + '/get_last_client_version'

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
