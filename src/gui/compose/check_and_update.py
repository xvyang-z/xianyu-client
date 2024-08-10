import hashlib
import os
import shutil
from os.path import join, relpath, normpath

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QWidget, QDialog, QMessageBox

import settings
from api.update import get_remote_file_info, download_update_file, check_update
from gui.uipy.update import Ui_Dialog
from settings import ROOT_DIR


def file_md5(file_path):
    """计算文件的MD5值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_local_file_info() -> dict[str, str]:
    """
    获取本地文件及其MD5值
    :return: 该目录下所有文件路径(相对于root_dir) 和 md5 的对应关系
    """
    # {文件的绝对路径: 文件md5}
    local_files_to_md5: dict[str: str] = {}

    for parent_dir, all_dir_name, all_file_name in os.walk(ROOT_DIR):
        for file_name in all_file_name:
            abs_file_path = join(parent_dir, file_name)  # 用 绝对路径 去找文件计算md5
            rel_file_dir = relpath(str(abs_file_path), ROOT_DIR)
            norm_rel_file_path = normpath(rel_file_dir).replace(os.sep, '/')  # 去除 . .. 并 将路径分隔符替换成 /

            local_files_to_md5[norm_rel_file_path] = file_md5(abs_file_path)

    return local_files_to_md5


class StartUpdate(QThread):
    downloaded_size = Signal(int)  # 每下载一个文件, 提交一次信号, 该值为此次下载文件的大小, 单位: byte
    finished = Signal(bool, str)  # 全部完成后提交一次, 或有意外出错时也提交

    def __init__(
            self,
            diff_file_info: list[get_remote_file_info.FileInfo],
            remote_file_info: list[get_remote_file_info.FileInfo],
            local_file_info: dict[str, str],
    ):
        super().__init__()
        self.diff_file_info = diff_file_info
        self.local_file_info = local_file_info
        self.remote_file_info = remote_file_info

    def run(self):
        ok, msg = self.sync_files()
        self.finished.emit(ok, msg)

    def sync_files(self) -> tuple[bool, str]:
        # 下载或更新文件
        for file_info in self.diff_file_info:
            ok, msg = download_update_file.download_update_file(file_info.file)
            if ok:
                self.downloaded_size.emit(file_info.size)
            else:
                return False, msg

        # 保存所有远程文件的信息, 以便更新程序可以清理未用到的文件
        with open(settings.ALL_REMOTE_FILE, 'w') as f:
            for file_info in self.remote_file_info:
                f.write(file_info.file + '\n')

        return True, ''


class UpdateDialog(QDialog, Ui_Dialog):
    def __init__(self, update_info: str, remote_file_info: list[get_remote_file_info.FileInfo]):
        """
        :param update_info: 展示本次更新的详情, 可以是一段 html
        :param remote_file_info: 服务端的文件信息
        """
        super().__init__()
        self.setupUi(self)

        self.update_info = update_info
        self.remote_file_info = remote_file_info
        self.local_file_info = get_local_file_info()

        self.setWindowTitle('更新')
        self.update_info_text_edit.setHtml(update_info)
        self.update_info_text_edit.setEnabled(False)
        self.progress.setVisible(False)
        self.progress_text.setVisible(False)

        # 计算差异文件
        self.diff_file_info: list[get_remote_file_info.FileInfo] = []
        for file_info in self.remote_file_info:
            if (
                    file_info.file not in self.local_file_info.keys()
                    or self.local_file_info[file_info.file] != file_info.md5
            ):
                self.diff_file_info.append(file_info)

        # 在更新按钮上显示大小信息
        self.already_downloaded_size = 0
        self.total_size = sum([i.size for i in self.diff_file_info])
        self.accept_btn.setText(self.accept_btn.text() + f' ({self.total_size / 1000000:.2f} Mb)')

        self.accept_btn.clicked.connect(self.handle_accept_btn)
        self.ignor_btn.clicked.connect(self.close)

        self.progress.valueChanged.connect(lambda value: self.progress_text.setText(f'{value}%'))

        self.start_update_task = StartUpdate(
            self.diff_file_info,
            self.remote_file_info,
            self.local_file_info
        )
        self.start_update_task.downloaded_size.connect(self.update_process)
        self.start_update_task.finished.connect(self.update_finished)

    def handle_accept_btn(self):
        self.progress.setVisible(True)
        self.progress_text.setVisible(True)

        self.accept_btn.setEnabled(False)
        self.ignor_btn.setEnabled(False)

        self.start_update_task.start()

    def update_process(self, size: int):
        self.already_downloaded_size += size
        self.progress.setValue(
            int(self.already_downloaded_size / self.total_size * 100)
        )

    def update_finished(self, ok: bool, msg: str):
        if ok:
            self.progress.setValue(100)
            QMessageBox.information(
                self,
                '成功',
                '更新成功, 下次重启生效'
            )
        else:
            shutil.rmtree(settings.TEMP_UPDATE_DIR, True)  # 出错就删除所有已下载的文件, 下次重新下载
            QMessageBox.warning(
                self,
                '失败',
                '更新失败, 请检查网络或重启软件后重试!\n' + msg
            )
        self.close()


class CheckUpdate(QThread):
    finished = Signal(bool, object)

    def __init__(self, parent: QWidget = None, local_file_info: dict[str, str] = None):
        super().__init__(parent)
        self.local_file_info = local_file_info
        self.update_dialog: UpdateDialog | None = None
        self.finished.connect(self.handle_check_update_task_finished)

    def run(self):
        ok, result = check_update.check_update()
        self.finished.emit(ok, result)

    def handle_check_update_task_finished(self, ok: bool, result: check_update.Data | str):
        if ok and result.version != settings.VERSION:
            ok, result = get_remote_file_info.get_remote_file_info()
            if ok:
                self.update_dialog = UpdateDialog(result.update_info, result.file_info)
                self.update_dialog.exec()  # app级 模态
