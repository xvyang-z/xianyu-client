import requests

from settings import CLIENT_API
from util.request_lock import request_lock


@request_lock
def check_token_expire(token: str) -> tuple[bool, str]:
    """
    检查 token 的过期时间
    """
    try:
        resp = requests.post(
            url=f'{CLIENT_API}/check_token_expire',
            json={
                'token': token
            }
        )
        if resp.json()['code'] == 0:
            return True, resp.json()['data']
        else:
            return False, resp.json()['message']
    except Exception as e:
        return False, f'未知错误 {e}'
