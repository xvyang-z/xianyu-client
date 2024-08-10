import sys

import PySide6
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QApplication, QTableWidgetItem

from gui.uipy import home
from handle import device_task_queue, device_thread_running, device_flag_to_name
from settings import ADB_TCP_PORT_SUFFIX


class Home(QWidget, home.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        cols = ['设备名', '设备标识', '剩余任务数']
        self.tableWidget.setColumnCount(len(cols))
        self.tableWidget.setHorizontalHeaderLabels(cols)

        # 设置定时器定时刷新 table
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(1000)  # 1000ms = 1s

    def refresh(self):
        # 先清除表格之前所有数据
        self.tableWidget.setRowCount(0)

        # 晒选正在运行的设备
        running_device = [k for k, v in device_thread_running.items() if v]

        # 在填充数据前设置数据条数, 不然不显示
        self.tableWidget.setRowCount(len(running_device))

        # 填充表格数据
        for row, device_flag in enumerate(running_device):
            for col, data in enumerate([
                device_flag_to_name[device_flag],
                device_flag.replace(ADB_TCP_PORT_SUFFIX, ''),
                str(device_task_queue[device_flag].qsize() + 1)
            ]):
                item = QTableWidgetItem(data)
                item.setFlags(item.flags() & ~ PySide6.QtCore.Qt.ItemFlag.ItemIsEditable)  # 设为不可编辑
                item.setTextAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)  # 设置文字居中
                self.tableWidget.setItem(row, col, item)

    def quit(self):
        self.close()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Home()
    window.show()
    sys.exit(app.exec())
