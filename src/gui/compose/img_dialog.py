import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QApplication


class ImgDialog(QDialog):
    def __init__(self, parent, img_path: Path, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.setGeometry(100, 100, 500, 300)
        self.setWindowTitle("步骤图片")
        self.setMinimumSize(400, 500)

        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pixmap = QPixmap(str(img_path))
        self.label.setPixmap(self.pixmap)

        layout.addWidget(self.label)
        self.setLayout(layout)

    def resizeEvent(self, a0, QResizeEvent=None):
        label_width = self.label.width()
        label_height = self.label.height()

        # 计算pixmap的新尺寸，同时保持纵横比
        pixmap_size = self.pixmap.size()
        aspect_ratio = pixmap_size.width() / pixmap_size.height()

        if label_width / aspect_ratio <= label_height:
            new_width = label_width
            new_height = int(label_width / aspect_ratio)
        else:
            new_width = int(label_height * aspect_ratio)
            new_height = label_height

        scaled_pixmap = self.pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.label.setPixmap(scaled_pixmap)

        super().resizeEvent(QResizeEvent)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImgDialog(None, Path(r'C:\Users\z\Desktop\xianyu-script\client\.resource\step_img\step1.jpg'))
    window.show()
    sys.exit(app.exec())
