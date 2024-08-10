import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Union

import uiautomator2
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QWidget, QApplication, QPushButton, QMessageBox
from uiautomator2 import Device

from gui.compose.img_dialog import ImgDialog
from settings import ASSERT_DIR, ADB_TCP_PORT
from gui.uipy import new_phone_start


def _获取USB设备标识符() -> tuple[bool, str]:
    cmd = ['adb.exe', 'devices']
    cmd_process = subprocess.run(cmd, capture_output=True, text=True)

    if cmd_process.returncode != 0:
        return False, '查看 adb 设备失败'

    devices_info = cmd_process.stdout.strip().splitlines()[1:]

    usb_device_count = 0
    usb_device_flag = ''
    for item in devices_info:
        device_flag, name = item.split('\t')
        if ':' not in device_flag:
            usb_device_flag = device_flag
            usb_device_count += 1

    if usb_device_count == 0:
        return False, '未检测到usb设备, 请确认手机打开usb调试, 并用usb连接电脑后, 在手机上允许调试'
    if usb_device_count > 1:
        return False, 'usb连接的设备只能有1台'

    return True, usb_device_flag


def _安装ATX(device_flag: str) -> tuple[bool, Union[Device, str]]:

    try:
        d = uiautomator2.connect(device_flag)
        return True, d
    except Exception as e:
        return False, f'安装失败{e}'


def _开启无线调试(usb_device_flag: str) -> tuple[bool, str]:
    # 开启无线调试, 端口 5555
    cmd = ['adb.exe', '-s', usb_device_flag, 'tcpip', str(ADB_TCP_PORT)]
    cmd_process = subprocess.run(cmd, capture_output=True, text=True)

    if cmd_process.returncode != 0 or cmd_process.stdout != f'restarting in TCP mode port: {ADB_TCP_PORT}\n':
        return False, '打开无线调试失败'

    return True, ''


def _获取无线设备标识符(usb_device_flag: str) -> tuple[bool, str]:
    """
    这里对用户隐藏 :5555 端口, 仅给出 ip, 在网页上添加时会自动带上 :5555
    也就是用户全程感知不到有这个端口, 仅看得到 ip, 更加直观
    """
    cmd = ["adb.exe", "-s", usb_device_flag, "shell", "ip", "addr", "show", "wlan0"]

    time.sleep(2)  # 上一步打开无限调试后, 手机端会短暂重启, 这里等一下再去执行
    cmd_process = subprocess.run(cmd, capture_output=True, text=True)
    if cmd_process.returncode != 0:
        return False, f'查看usb设备的ip时出错: {cmd_process.stdout} {cmd_process.stderr}'

    text = cmd_process.stdout

    result = re.findall(r'inet (.*?)/', text)
    if not result:
        return False, '请确认手机已连接无线局域网并获取到ip'
    ip: str = result[0]

    # wireless_adb_device_flag = f'{ip}:{ADB_TCP_PORT}'
    # return True, wireless_adb_device_flag

    return True, ip


class _IninInstall(QThread):
    """
    执行初始化安装
    """
    init_install_finished = Signal(bool, str)

    def __init__(self):
        super().__init__()

    def run(self):
        ok, usb_devices_flag = _获取USB设备标识符()
        if not ok:
            self.init_install_finished.emit(False, usb_devices_flag)
            return

        success, device = _安装ATX(usb_devices_flag)
        if not success:
            self.init_install_finished.emit(False, device)
            return

        self.init_install_finished.emit(True, device)
        return


class _OpenWirelessDebug(QThread):
    open_wireless_debug_finished = Signal(bool, str)

    def __init__(self):
        super().__init__()

    def run(self):
        ok, usb_devices_flag = _获取USB设备标识符()
        if not ok:
            self.open_wireless_debug_finished.emit(False, usb_devices_flag)
            return

        ok, info = _开启无线调试(usb_devices_flag)
        if not ok:
            self.open_wireless_debug_finished.emit(False, info)
            return

        ok, ip = _获取无线设备标识符(usb_devices_flag)
        if not ok:
            self.open_wireless_debug_finished.emit(False, ip)
            return

        self.open_wireless_debug_finished.emit(True, ip)
        return


class NewPhoneStart(QWidget, new_phone_start.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.show_img_btn_1: QPushButton
        self.show_img_btn_2: QPushButton
        self.show_img_btn_3: QPushButton
        self.show_img_btn_4: QPushButton
        self.show_img_btn_6: QPushButton

        self.init_install_btn: QPushButton
        self.open_wireless_debug_btn: QPushButton

        self.show_img_btn_1.clicked.connect(lambda: self.__show_img_dialog(ASSERT_DIR / './step_img/step1.jpg'))
        self.show_img_btn_2.clicked.connect(lambda: self.__show_img_dialog(ASSERT_DIR / './step_img/step2.jpg'))
        self.show_img_btn_4.clicked.connect(lambda: self.__show_img_dialog(ASSERT_DIR / './step_img/step4.jpg'))
        self.show_img_btn_5_1.clicked.connect(lambda: self.__show_img_dialog(ASSERT_DIR / './step_img/step5_1.jpg'))
        self.show_img_btn_5_2.clicked.connect(lambda: self.__show_img_dialog(ASSERT_DIR / './step_img/step5_2.jpg'))

        self.init_install_btn.clicked.connect(self.__handle_init_install)
        self.open_wireless_debug_btn.clicked.connect(self.__handle_open_wireless_debug)

        self.init_install_task = _IninInstall()
        self.init_install_task.init_install_finished.connect(self.__handle_init_install_finished)

        self.oppen_wireless_debug_task = _OpenWirelessDebug()
        self.oppen_wireless_debug_task.open_wireless_debug_finished.connect(self.__handle_open_wireless_debug_finished)

    def __show_img_dialog(self, img_path: Path):
        if not os.path.exists(img_path):
            QMessageBox.warning(self, '找不到文件', '图片丢失或损坏', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return

        ImgDialog(self, img_path).show()

    def __handle_init_install(self):
        self.init_install_btn.setEnabled(False)
        self.init_install_task.start()

    def __handle_init_install_finished(self, ok, info):
        self.init_install_btn.setEnabled(True)

        if ok:
            QMessageBox.information(self, '成功', f'初始化安装完成 {info}', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.warning(self, '失败', f'初始化安装失败 {info}', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)

    def __handle_open_wireless_debug(self):
        self.open_wireless_debug_btn.setEnabled(False)
        self.oppen_wireless_debug_task.start()

    def __handle_open_wireless_debug_finished(self, ok, info):
        self.open_wireless_debug_btn.setEnabled(True)

        if ok:
            QMessageBox.information(self, '成功', f'无线设备标识: {info}', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.warning(self, '失败', f'错误 {info}', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NewPhoneStart()
    window.show()
    sys.exit(app.exec())
