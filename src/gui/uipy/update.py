# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'update.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QTextEdit, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(426, 410)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.update_info_text_edit = QTextEdit(Dialog)
        self.update_info_text_edit.setObjectName(u"update_info_text_edit")

        self.verticalLayout.addWidget(self.update_info_text_edit)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.progress = QProgressBar(self.widget)
        self.progress.setObjectName(u"progress")
        self.progress.setValue(0)
        self.progress.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.progress.setTextVisible(False)
        self.progress.setOrientation(Qt.Orientation.Horizontal)
        self.progress.setInvertedAppearance(False)

        self.verticalLayout_2.addWidget(self.progress)

        self.progress_text = QLabel(self.widget)
        self.progress_text.setObjectName(u"progress_text")
        self.progress_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.progress_text)


        self.verticalLayout.addWidget(self.widget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ignor_btn = QPushButton(Dialog)
        self.ignor_btn.setObjectName(u"ignor_btn")
        self.ignor_btn.setMinimumSize(QSize(0, 30))
        self.ignor_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.ignor_btn.setMouseTracking(True)
        self.ignor_btn.setAutoFillBackground(False)
        self.ignor_btn.setStyleSheet(u":hover{\n"
"color:rgb(40, 60, 240);\n"
"}")
        self.ignor_btn.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.ignor_btn)

        self.accept_btn = QPushButton(Dialog)
        self.accept_btn.setObjectName(u"accept_btn")
        self.accept_btn.setMinimumSize(QSize(0, 30))
        self.accept_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.accept_btn.setAutoFillBackground(False)
        self.accept_btn.setStyleSheet(u"QPushButton{\n"
"background:rgb(46, 140, 240);\n"
"color: #fff;\n"
"}\n"
":hover{\n"
"background:rgb(60, 160, 240);\n"
"}")
        self.accept_btn.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.accept_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u6709\u66f4\u65b0\u53ef\u7528", None))
        self.update_info_text_edit.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">(\u65e0\u66f4\u65b0\u4fe1\u606f)</p></body></html>", None))
        self.progress.setFormat(QCoreApplication.translate("Dialog", u"%p%", None))
        self.progress_text.setText("")
        self.ignor_btn.setText(QCoreApplication.translate("Dialog", u"\u7a0d\u540e\u66f4\u65b0", None))
        self.accept_btn.setText(QCoreApplication.translate("Dialog", u"\u7acb\u5373\u66f4\u65b0", None))
    # retranslateUi

