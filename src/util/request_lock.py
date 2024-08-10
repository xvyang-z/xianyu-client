import threading

lock = threading.Lock()


def request_lock(func):
    """
    请求锁, 确保同一时间仅有一个请求和服务器交互

    例如在 任务完成 后 会向服务器发送成功的消息, 此时另一线程 get_task 可能会提前到达服务器并获取到响应, 也就是任务会被执行两次, 用这个锁来避免这种情况
    """

    def warp(*args, **kwargs):
        lock.acquire()

        try:
            result = func(*args, **kwargs)
        finally:
            lock.release()

        return result

    return warp
