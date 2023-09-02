from PyQt5.QtGui import QFont, QPainter, QColor, QBrush
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPointF
from PyQt5.Qt import QFontDatabase

import DataManager
import resourses
class PageAuthorization(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.koefW, self.koefH = 1, 1
        self.iduser = ""
        fontId = QFontDatabase.addApplicationFont("Fonts/Circe-Regular.ttf")
        Circle_Regular = QFontDatabase.applicationFontFamilies(fontId)[0]

        shadow = QGraphicsDropShadowEffect(self,
                                                     blurRadius=35,
                                                     color=QColor(0, 0, 0, 35),
                                                     offset=QPointF(10, 10),
                                                     )
        self.setGraphicsEffect(shadow)

        self.lAuthorization = QLabel(self)
        self.lAuthorization.move(400, 110)
        self.lAuthorization.resize(300, 40)
        self.lAuthorization.setText('Авторизация')
        self.lAuthorization.setAlignment(Qt.AlignCenter)
        self.lAuthorization.setFont(QFont(Circle_Regular, 20))

        self.inLogIn = QLineEdit(self)
        self.inLogIn.move(400, 170)
        self.inLogIn.resize(300, 60)
        self.inLogIn.setPlaceholderText('Логин')
        self.inLogIn.setText('admin')
        self.inLogIn.setFont(QFont(Circle_Regular, 14))

        self.inPass = QLineEdit(self)
        self.inPass.move(400, 250)
        self.inPass.resize(300, 60)
        self.inPass.setPlaceholderText('Пароль')
        self.inPass.setText('admin')
        self.inPass.setFont(QFont('Circle_Regular', 14))
        self.inPass.setEchoMode(QLineEdit.Password)

        self.butLogIn = QPushButton('Войти', self)
        self.butLogIn.resize(300, 60)
        self.butLogIn.move(400, 330)
        self.butLogIn.setFont(QFont('Circle_Regular', 16))
        self.butLogIn.setStyleSheet("QPushButton {background-color: rgb(235,86,79); color: White; border-radius: 1px;}"
                           "QPushButton:pressed {background-color:rgb(251,114,107) ; }")
        self.SetNormalSize()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)  # Рисование фигур
        qp.end()

    def drawRectangles(self, qp):
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)  # Установка карандаша

        qp.setBrush(QColor(254, 254, 254))  # Установка кисти
        qp.drawRoundedRect(int(375 * self.koefW), int(75 * self.koefH), int(350 * self.koefW), int(350 * self.koefH), 10, 10)   # Рисование прямоугольника

    def messageboxerror(self, text):
        msg = QMessageBox.critical(self, "Ошибка ", text, QMessageBox.Ok)
        return False

    def LogIn(self):
        login = self.inLogIn.text()
        password = self.inPass.text()
        id = DataManager.select_users_where("id", "login='" + login + "' AND password='" + password + "'")
        if id:
            self.iduser = id[0][0]
            return True
        else:
            self.messageboxerror("Возникли проблемы с авторизацией")

    def LogOut(self):
        self.inLogIn.setText("")
        self.inPass.setText("")


    def SetNormalSize(self):
        for i in self.children():
            try:
                i.x0 = i.x()
                i.y0 = i.y()
                i.width0 = i.width()
                i.height0 = i.height()
            except:
                print("Normal size missed " + str(i))
    def DynamicSize(self, koefW, koefH):
        for i in self.children():
            try:
                i.resize(int(i.width0 * koefW), int(i.height0 * koefH))
                i.move(int(i.x0 * koefW), int(i.y0 * koefH))
                self.koefW = koefW
                self.koefH = koefH

            except:
                print("Dynamic size missed " + str(i))