from api.exec_fail import exec_fail
from api.check_token_expire import check_token_expire
from api.get_task import get_task
from api.upload_file import upload_file

from api import success

from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar('T')


class BaseResp(BaseModel, Generic[T]):
    code: int
    message: str
    data: T
