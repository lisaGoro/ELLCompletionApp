from datetime import datetime
from PyQt5.QtWidgets import *

import DataManager


class PageInput1(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.lCompany = QLabel(self)
        self.lCompany.move(20, 20)
        self.lCompany.setText('Компания')
        self.inCompany = QLineEdit(self)
        self.inCompany.move(20, 40)
        self.inCompany.resize(450, 40)
        self.inCompany.setPlaceholderText('Компания')

        self.lField = QLabel(self)
        self.lField.move(490, 20)
        self.lField.setText('Месторождение')
        self.inField = QLineEdit(self)
        self.inField.move(490, 40)
        self.inField.resize(450, 40)
        self.inField.setPlaceholderText('Месторождение')

        self.lWell = QLabel(self)
        self.lWell.move(20, 100)
        self.lWell.setText('Скважина')
        self.inWell = QLineEdit(self)
        self.inWell.move(20, 120)
        self.inWell.resize(450, 40)
        self.inWell.setPlaceholderText('Скважина')

        self.lBush = QLabel(self)
        self.lBush.move(490, 100)
        self.lBush.setText('Куст')
        self.inBush = QLineEdit(self)
        self.inBush.move(490, 120)
        self.inBush.resize(450, 40)
        self.inBush.setPlaceholderText('Куст')

        self.lDate = QLabel(self)
        self.lDate.move(20, 180)
        self.lDate.setText('Дата подбора')
        self.inData = QDateEdit(self)
        self.inData.setDate(datetime.now())
        self.inData.setCalendarPopup(True)
        self.inData.move(20, 200)
        self.inData.resize(293, 40)

        self.lEngineer = QLabel(self)
        self.lEngineer.move(333, 180)
        self.lEngineer.resize(200, 20)
        self.lEngineer.setText('Инженер по подбору')
        self.engineer_combo = QComboBox(self)
        self.engineer_combo.move(333, 200)
        self.engineer_combo.resize(293, 40)
        self.engineer_combo.setPlaceholderText('Инженер по подбору')

        self.lPhoneNumber = QLabel(self)
        self.lPhoneNumber.move(646, 180)
        self.lPhoneNumber.setText('Контактная информация')
        self.inPhoneNumber = QLineEdit(self)
        self.inPhoneNumber.move(646, 200)
        self.inPhoneNumber.resize(293, 40)
        self.inPhoneNumber.setPlaceholderText('Контактная информация')

        self.butLeft1 = QPushButton('Назад', self)
        self.butLeft1.move(20, 280)

        self.butNext1 = QPushButton('Далее', self)
        self.butNext1.move(865, 280)

        # События
        self.engineer_combo.activated[str].connect(self.onActivated)

        self.SetNormalSize()

    def messageboxerror(self, text):
        msg = QMessageBox.critical(self, "Ошибка ", text, QMessageBox.Ok)
        return

    def onActivated(self, text):
        contact = DataManager.sql_query("SELECT contact FROM users WHERE name='" + text + "';")
        if contact:
            self.inPhoneNumber.setText(contact[0][0])
        else:
            self.messageboxerror("Проблема с подключением к базе данных код 501")

    def cleanPage(self):
        self.inCompany.setText('')
        self.inBush.setText('')
        self.inWell.setText('')
        self.inField.setText('')


    def SetNormalSize(self):
        for i in self.children():
            try:
                i.x0 = i.x()
                i.y0 = i.y()
                i.width0 = i.width()
                i.height0 = i.height()
            except:
                print("Normal size missed " + i)
    def DynamicSize(self, koefW, koefH):
        for i in self.children():
            try:
                i.resize(int(i.width0 * koefW), int(i.height0 * koefH))
                i.move(int(i.x0 * koefW), int(i.y0 * koefH))

            except:
                print("Dynamic size missed " + i)