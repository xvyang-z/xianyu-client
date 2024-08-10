import os
import shutil
from pathlib import Path


VERSION = '0.0.1'

APPNAME = 'com.taobao.idlefish'

# 任务刷新的间隔时间 (秒)
SLEEP_TIME = 10

# ----------------------------------------------------------- 项目根目录(该文件所在目录)
ROOT_DIR = Path(__file__).parent

# ----------------------------------------------------------- 临时目录, 存放运行时产生的文件
DATA_DIR = ROOT_DIR.parent / 'data'

# 爬取的图片暂存位置
IMG_PATH = DATA_DIR / 'crawl_img'
# 临时的下载目录
DOWNLOAD_PATH = DATA_DIR / 'download'

# 用户的 设置文件
USER_CONFIG_FILE = DATA_DIR / 'user.json'
# 更新软件 时用到的 私钥
PRIVATE_KEY_FILE = DATA_DIR / 'private.key'
# 更新文件的目录, 应用更新后会自动删除
TEMP_UPDATE_DIR = DATA_DIR / 'temp_update'
ALL_REMOTE_FILE = TEMP_UPDATE_DIR / 'all_remote_file.txt'

# ----------------------------------------------------------- gui相关
# gui 用到的 资源目录
ASSERT_DIR = ROOT_DIR / '.assets'

# ----------------------------------------------------------- 服务端通信相关
SERVER_HOST = 'http://192.168.0.31'

# 服务端的客户端api路由前缀
CLIENT_API = SERVER_HOST + '/client_api'

# 请求头
API_HEADER = {
    'Authorization': ''
}

# ----------------------------------------------------------- adb无线连接默认的端口, 和服务端的保持一致
ADB_TCP_PORT = 5555
ADB_TCP_PORT_SUFFIX = f':{ADB_TCP_PORT}'


# ----------------------------------------------------------- 初始化
def __init():
    # 将 adb 可执行文件添加到环境变量
    git_path = str(ASSERT_DIR / 'adb')
    os.environ['PATH'] = git_path + os.pathsep + os.environ['PATH']

    # 删除 临时图片 和 临时下载目录, 并重新创建
    shutil.rmtree(IMG_PATH, ignore_errors=True)
    shutil.rmtree(DOWNLOAD_PATH, ignore_errors=True)

    path_list = [IMG_PATH, DOWNLOAD_PATH]
    for path in path_list:
        if not os.path.exists(path):
            os.makedirs(path)


__init()
