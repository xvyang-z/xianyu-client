import os

import requests

from settings import TEMP_UPDATE_DIR, CLIENT_API, API_HEADER


def download_update_file(file_path: str) -> tuple[bool, str]:
    """下载文件的函数"""
    try:
        url = CLIENT_API + '/download_update_file'
        resp = requests.post(
            url,
            json={
                'file_path': file_path
            },
            headers=API_HEADER,
        )

        abs_file_path = TEMP_UPDATE_DIR / file_path

        # 如果父级目录不存在, 则创建它们
        if not abs_file_path.parent.exists():
            os.makedirs(abs_file_path.parent)

        with open(abs_file_path, 'wb') as f:
            f.write(resp.content)

        return True, ''

    except Exception as e:
        return False, str(e)
