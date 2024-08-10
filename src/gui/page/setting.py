import sys

from PySide6.QtCore import Signal, QThread, QTimer
from PySide6.QtWidgets import QWidget, QPushButton, QMessageBox, QLineEdit, QLabel, QApplication

import api
import settings
from gui.uipy import setting
from util.connect_state import ConnectState
from util.user_config import user_config


class _CheckToken(QThread):
    """
    检查 token 是否有效
    """
    check_token_finished = Signal(bool, str)

    def __init__(self):
        super().__init__()
        self.token = None

    def run(self):
        ok, info = api.check_token_expire(self.token)
        self.check_token_finished.emit(ok, info)


class Setting(QWidget, setting.Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.token_edit.setText(user_config.token)

        self.check_token_btn.clicked.connect(self.handle_check_token_btn)

        self.check_token_task = _CheckToken()
        self.check_token_task.check_token_finished.connect(self.handle_check_token_finished)

        # 设置定时器定时刷新连接状态
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_connect_server_info)
        self.timer.start(1000)  # 1000ms = 1s

    def handle_check_token_btn(self):
        """
        开始 检查token
        """
        self.token_edit.setEnabled(False)
        self.check_token_btn.setEnabled(False)

        self.check_token_task.token = self.token_edit.text()
        self.check_token_task.start()

    def handle_check_token_finished(self, ok: bool, info: str):
        """
        完成 检查token
        """
        self.token_edit.setEnabled(True)
        self.check_token_btn.setEnabled(True)
        if ok:
            token = self.token_edit.text()
            settings.API_HEADER = {
                'Authorization': token
            }
            user_config.token = token
            QMessageBox.information(self, '成功', 'token有效, 已保存')
        else:
            QMessageBox.warning(self, '失败', 'token无效' + info)

    def refresh_connect_server_info(self):
        """
        刷新服务器连接状态
        """
        if ConnectState.ok:
            self.connect_server_info.setText(f'<span style="color: #22cc22;">{ConnectState.info}</span>')
        else:
            self.connect_server_info.setText(f'<span style="color: #cc2222;">{ConnectState.info}</span>')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Setting()
    window.show()
    sys.exit(app.exec())
