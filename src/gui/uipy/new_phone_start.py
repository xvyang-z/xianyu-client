# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_phone_start.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(417, 647)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 385, 668))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.label)

        self.widget = QWidget(self.scrollAreaWidgetContents)
        self.widget.setObjectName(u"widget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy2)
        self.widget.setMinimumSize(QSize(0, 23))
        self.show_img_btn_1 = QPushButton(self.widget)
        self.show_img_btn_1.setObjectName(u"show_img_btn_1")
        self.show_img_btn_1.setGeometry(QRect(0, 0, 75, 23))

        self.verticalLayout_2.addWidget(self.widget)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.label_3)

        self.widget_2 = QWidget(self.scrollAreaWidgetContents)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy2.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy2)
        self.widget_2.setMinimumSize(QSize(0, 23))
        self.show_img_btn_2 = QPushButton(self.widget_2)
        self.show_img_btn_2.setObjectName(u"show_img_btn_2")
        self.show_img_btn_2.setGeometry(QRect(0, 0, 75, 23))

        self.verticalLayout_2.addWidget(self.widget_2)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")
        sizePolicy1.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.label_5)

        self.widget_6 = QWidget(self.scrollAreaWidgetContents)
        self.widget_6.setObjectName(u"widget_6")
        sizePolicy2.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy2)
        self.widget_6.setMinimumSize(QSize(0, 23))
        self.open_wireless_debug_btn = QPushButton(self.widget_6)
        self.open_wireless_debug_btn.setObjectName(u"open_wireless_debug_btn")
        self.open_wireless_debug_btn.setGeometry(QRect(0, 0, 91, 23))

        self.verticalLayout_2.addWidget(self.widget_6)

        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.label_4)

        self.widget_3 = QWidget(self.scrollAreaWidgetContents)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy2.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy2)
        self.widget_3.setMinimumSize(QSize(0, 23))
        self.show_img_btn_4 = QPushButton(self.widget_3)
        self.show_img_btn_4.setObjectName(u"show_img_btn_4")
        self.show_img_btn_4.setGeometry(QRect(0, 0, 75, 23))
        self.init_install_btn = QPushButton(self.widget_3)
        self.init_install_btn.setObjectName(u"init_install_btn")
        self.init_install_btn.setGeometry(QRect(100, 0, 75, 23))

        self.verticalLayout_2.addWidget(self.widget_3)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")
        sizePolicy1.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.label_6)

        self.widget_4 = QWidget(self.scrollAreaWidgetContents)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy2.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy2)
        self.widget_4.setMinimumSize(QSize(0, 23))
        self.show_img_btn_5_1 = QPushButton(self.widget_4)
        self.show_img_btn_5_1.setObjectName(u"show_img_btn_5_1")
        self.show_img_btn_5_1.setGeometry(QRect(0, 0, 75, 23))

        self.verticalLayout_2.addWidget(self.widget_4)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.label_2)

        self.widget_5 = QWidget(self.scrollAreaWidgetContents)
        self.widget_5.setObjectName(u"widget_5")
        sizePolicy2.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy2)
        self.widget_5.setMinimumSize(QSize(0, 23))
        self.show_img_btn_5_2 = QPushButton(self.widget_5)
        self.show_img_btn_5_2.setObjectName(u"show_img_btn_5_2")
        self.show_img_btn_5_2.setGeometry(QRect(0, 0, 75, 23))

        self.verticalLayout_2.addWidget(self.widget_5)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"<html><head/><body><h4 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:600;\">1 \u6253\u5f00USB\u8c03\u8bd5</span></h4><p>1. \u6253\u5f00 - \u5f00\u53d1\u8005\u6a21\u5f0f<br/>2. \u6253\u5f00 - USB\u8c03\u8bd5<br/>3. \u6253\u5f00 - USB\u5b89\u88c5<br/>4. \u6253\u5f00 - USB\u8c03\u8bd5(\u5b89\u5168\u8bbe\u7f6e)</p></body></html>", None))
        self.show_img_btn_1.setText(QCoreApplication.translate("Form", u"\u67e5\u770b\u56fe\u7247", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"<html><head/><body><hr/><h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:600;\">2 \u5141\u8bb8\u8c03\u8bd5</span></h3><p>1. \u63d2\u5165USB\u7ebf, \u786e\u4fdd\u7535\u8111\u6b64\u65f6\u53ea\u6709\u4e00\u4e2aAndroid\u8bbe\u5907\u7528USB\u8fde\u63a5<br/>2. \u5728\u624b\u673a\u4e0a\u70b9\u51fb\u5141\u8bb8\u8c03\u8bd5</p></body></html>", None))
        self.show_img_btn_2.setText(QCoreApplication.translate("Form", u"\u67e5\u770b\u56fe\u7247", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"<html><head/><body><hr/><h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:600;\">3 \u5f00\u542f\u65e0\u7ebf\u8c03\u8bd5</span></h3><p>1. \u5f00\u542f\u65e0\u7ebf\u8c03\u8bd5 <br/>2. \u5f53\u624b\u673a\u5173\u673a\u518d\u5f00\u673a\u9700\u8981\u7528USB\u7ebf\u8fde\u63a5\u7535\u8111, \u4e14\u4ec5\u6267\u884c\u8fd9\u4e00\u6b65\u5373\u53ef</p></body></html>", None))
        self.open_wireless_debug_btn.setText(QCoreApplication.translate("Form", u"\u5f00\u542f\u65e0\u7ebf\u8c03\u8bd5", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"<html><head/><body><hr/><h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:600;\">4 \u521d\u59cb\u5316\u5b89\u88c5</span></h3><p>1. \u70b9\u51fb\u4e0b\u65b9`\u521d\u59cb\u5316\u5b89\u88c5`, \u4f1a\u5b89\u88c5\u4e24\u4e2a\u63a7\u5236\u8f6f\u4ef6\u548c\u5bf9\u5e94\u7248\u672c\u95f2\u9c7c<br/>2. \u6b64\u65f6\u5728\u624b\u673a\u4e0a\u5f39\u51fa\u662f\u5426\u5b89\u88c5\u7684\u8be2\u95ee\u5f39\u7a97, \u8bf7\u5168\u90e8\u9009\u62e9\u7ee7\u7eed\u5b89\u88c5</p></body></html>", None))
        self.show_img_btn_4.setText(QCoreApplication.translate("Form", u"\u67e5\u770b\u56fe\u7247", None))
        self.init_install_btn.setText(QCoreApplication.translate("Form", u"\u521d\u59cb\u5316\u5b89\u88c5", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"<html><head/><body><hr/><h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:600;\">5 \u5176\u4ed6\u8bbe\u7f6e</span></h3><p>1. \u8bbe\u7f6e\u6c38\u4e0d\u606f\u5c4f (\u811a\u672c\u5728\u606f\u5c4f\u72b6\u6001\u65e0\u6cd5\u6267\u884c)</p></body></html>", None))
        self.show_img_btn_5_1.setText(QCoreApplication.translate("Form", u"\u67e5\u770b\u56fe\u7247", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>2. \u5728\u5f00\u53d1\u8005\u6a21\u5f0f\u4e2d\u5c06\u624b\u673a\u7684\u52a8\u753b\u6548\u679c\u5173\u95ed, \u4f7f\u811a\u672c\u8fd0\u884c\u5f97\u66f4\u5feb</p></body></html>", None))
        self.show_img_btn_5_2.setText(QCoreApplication.translate("Form", u"\u67e5\u770b\u56fe\u7247", None))
    # retranslateUi

