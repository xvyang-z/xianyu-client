import PySide6
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QListWidget, QStackedWidget, QListWidgetItem, QMessageBox, QInputDialog

from gui.compose.check_and_update import CheckUpdate
from gui.page import home
from gui.page import new_phone_start
from gui.page import setting
from gui.uipy import main
from handle import device_thread_running
from settings import ASSERT_DIR


class Main(QWidget, main.Ui_Form):
    """
    左侧选项, 右侧层叠窗口的框架界面
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 检查更新的task, 有更新会弹出 dialog
        self.check_update_task = CheckUpdate(self)
        self.check_update_task.start()

        self.setWindowTitle("闲鱼助手客户端")

        self.name_and_tip = {
            '运行中': '查看当前正在运行的设备',
            '初始化': '新设备初始化指引',
            '设置': '系统运行的参数',
        }

        self.pages = [
            home.Home(),
            new_phone_start.NewPhoneStart(),
            setting.Setting(),
        ]

        self.setWindowIcon(QIcon(str(ASSERT_DIR / 'gui_icon.svg')))

        self.set_left_bar()
        self.set_right_window()

    def set_left_bar(self):
        """
        设置左侧选项栏
        :return:
        """

        # 通过QListWidget的当前item变化来切换QStackedWidget中的序号
        self.listWidget.currentRowChanged.connect(self.stackedWidget.setCurrentIndex)

        # 去掉边框
        self.listWidget.setFrameShape(PySide6.QtWidgets.QFrame.Shape.NoFrame)
        # 隐藏滚动条
        self.listWidget.setVerticalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        for name, tip in self.name_and_tip.items():
            item = QListWidgetItem(name, self.listWidget)
            # 设置item的默认宽高(上面固定了宽度, 这里只有高度有用)
            item.setSizeHint(QSize(0, 40))
            # 设置文本对齐方式为居中
            item.setTextAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)
            # 鼠标停留时的提示
            item.setToolTip(tip)

        # 添加好元素后, 设置默认选中
        self.listWidget.setCurrentRow(0)

    def set_right_window(self):
        """
        设置右侧窗口, 要和左侧选项对应
        :return:
        """
        # 设置左边距 20
        self.stackedWidget.setContentsMargins(20, 0, 0, 0)

        # 添加界面
        for page in self.pages:
            self.stackedWidget.addWidget(page)

        # 添加好元素后, 设置默认选中 0
        self.stackedWidget.setCurrentIndex(0)

    def closeEvent(self, event, **kwargs):
        device_thread_running_values = device_thread_running.values()

        if device_thread_running_values and any(device_thread_running_values):
            text, ok = QInputDialog.getText(
                self,
                '严重警告',
                '当前有任务正在运行, 强行退出会造成数据错乱!!!\n若要强退出行请输入 "确认退出" 关闭程序:'
            )

            if ok and text == '确认退出':
                reply = QMessageBox.warning(
                    self,
                    '再次确认',
                    '当前有任务正在运行, 强行退出会造成数据错乱!!!\n仍要退出?',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No,
                )
                if reply == QMessageBox.StandardButton.Yes:

                    # 销毁窗口前确认进程结束, 未结束需要手动停止, 否则应用会崩溃, 虽然都要退出了, 还是手动关闭下比较好
                    if self.check_update_task.isRunning():
                        self.check_update_task.terminate()
                        self.check_update_task.wait()

                    event.accept()
                else:
                    event.ignore()
            else:
                QMessageBox.information(
                    self,
                    '未退出',
                    '输入错误, 程序未退出'
                )
                event.ignore()
