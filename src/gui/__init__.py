import re
import sys

from PySide6.QtWidgets import QApplication, QMessageBox
import psutil
from gui.page.main import Main
from settings import ROOT_DIR


def is_already_running():
    current_process = psutil.Process()
    current_cmdline = current_process.cmdline()

    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if (
                True
                and process.pid != current_process.pid
                and process.name == current_process.name()
                and process.cmdline == current_cmdline
        ):
            return True
    return False


def run_gui():
    # 正常从启动程序启动会加上 --run 参数, 如果没有直接退出
    if '--run' not in sys.argv:
        return

    app = QApplication(sys.argv)

    if is_already_running():
        QMessageBox.warning(None, "警告", "程序已经在运行中", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        exit(0)

    if re.search(r'[\u4e00-\u9fff ]', str(ROOT_DIR)):
        QMessageBox.warning(None, '警告', '软件路径不能有中文或空格', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        exit(0)

    main = Main()
    main.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    run_gui()
