class ConnectState:
    """
    显示与服务器的连接状态

    从 handle 中更新
    从 gui 中读取
    """
    ok = False
    info = '连接中...'

    @staticmethod
    def update(ok: bool, info: str):
        ConnectState.ok = ok
        ConnectState.info = info
