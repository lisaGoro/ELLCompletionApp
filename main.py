import datetime

from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtWidgets import *

import DataManager
from PageInput1 import PageInput1
from PageInput2 import PageInput2
from PageOutput import PageOutput
from PageBigSheme import BigSheme
import FileCreating
from PageAuthorization import PageAuthorization
from PageProjects import PageProjects
from Data import Data

PrIn = Data.ProjectInfo()
HoIn = Data.HoleInfo()


def validateInt(str):
    try:
        if (str != ""):
            int(str)
        return True
    except BaseException:
        return False
def validateStr(str, count):
    if (len(str) > count):
        return False
    else:
        return True
def validateFloat(str):
    try:
        if (str != ""):
            float(str)
        return True
    except BaseException:
        return False


class TextEditDemo(QWidget):
    resized = pyqtSignal()
    def __init__(self, parent=None):
        super(TextEditDemo, self).__init__(parent)
        self.setWindowTitle("ELL COMPLETION APP")
        self.id = 0
        self.resize(1100, 550)
        self.setMinimumSize(1100, 550)
        self.oImage = QImage("icon/background.jpg").scaled(1920, 1080)
        self.SetBackgroundImg()

        self.pAuthorization = PageAuthorization()
        self.pProjects = PageProjects()
        self.pInput1 = PageInput1()
        self.pInput2 = PageInput2()
        self.pOutput = PageOutput()
        self.pBigSheme = BigSheme()
        self.setWindowIcon(QIcon('icon/Icon.ico'))


        self.widget = QWidget()
        self.page = QStackedLayout()
        self.widget.setLayout(self.page)
        self.page.addWidget(self.pAuthorization)
        self.page.addWidget(self.pProjects)
        self.page.addWidget(self.pInput1)
        self.page.addWidget(self.pInput2)
        self.page.addWidget(self.pOutput)
        self.page.addWidget(self.pBigSheme)

        layout = QVBoxLayout()
        layout.addWidget(self.widget)
        self.setLayout(layout)

        """
        Связи кнопок, событий и тд
        """
        self.resized.connect(self.DynamicSize)
        # авторизация
        self.pAuthorization.butLogIn.clicked.connect(self.butBaseProj_Clicked)
        self.pProjects.butLeft.clicked.connect(self.LogOut)
        # меню проектов
        self.pProjects.tableProjects.selectionModel().selectionChanged.connect(self.on_selectionChanged)
        self.pProjects.butOpenProj.clicked.connect(self.butOpenProj_Clicked)
        self.pProjects.butNewProj.clicked.connect(self.butNewProj_Clicked)
        self.pProjects.butDelProj.clicked.connect(self.on_deleted_Clicked)
        # создание нового проекта
        self.pInput1.butLeft1.clicked.connect(self.butLeft1_Clicked)
        self.pInput1.butNext1.clicked.connect(self.butNext1_Clicked)
        self.pInput2.butLeft2.clicked.connect(self.butLeft2_Clicked)
        self.pInput2.butNext2.clicked.connect(self.butNext2_Clicked)
        self.pOutput.butLeftCreateProject.clicked.connect(self.LeftOpenProject)
        # вывод составленной компоновки
        self.pOutput.shemeWid.clicked.connect(self.openSheme)
        self.pBigSheme.BackBackBut.clicked.connect(self.closeSheme)
        self.pOutput.butLeft.clicked.connect(self.LeftOpenProject)

    def messageboxerror(self, text):
        msg = QMessageBox.critical(self, "Ошибка ", text, QMessageBox.Ok)
        return

    def backBigSchema(self):
        self.page.setCurrentIndex(5)


    def SetBackgroundImg(self):
        sImage = self.oImage.scaled(QSize(self.width(), self.height()))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(self.oImage))
        self.setPalette(palette)

    def LogOut(self):
        self.pProjects.butOpenProj.setIcon(QIcon("icon/OpenFileInactive.png"))
        self.pAuthorization.LogOut()
        self.pInput1.engineer_combo.clear()
        self.page.setCurrentIndex(0)

    def butBaseProj_Clicked(self):
        if self.pAuthorization.LogIn():
            self.pProjects.iduser = self.pAuthorization.iduser
            access = DataManager.select_user_id("access", str(self.pProjects.iduser))
            if access:
                self.pProjects.access = access[0][0]
            else:
                self.messageboxerror("Возникли проблемы с соединением с базой данной код 1001")
            name = DataManager.select_user_id("name", str(self.pProjects.iduser))
            if name:
                self.pProjects.lwelcomename.setText(name[0][0])
            else:
                self.messageboxerror("Возникли проблемы с соединением с базой данной код 1002")
            users = DataManager.select_users_where("name", "access!='all'")
            if users:
                for user in users:
                    self.pInput1.engineer_combo.addItem(user[0])
            else:
                self.messageboxerror("Возникли проблемы с соединением с базой данной код 1003")
            if self.pProjects.access == "anything":
                self.pInput1.engineer_combo.setCurrentIndex(self.pInput1.engineer_combo.findText(name[0][0]))
                contact = DataManager.select_user_id("contact", str(self.pProjects.iduser))
                if contact:
                    self.pInput1.inPhoneNumber.setText(contact[0][0])
                else:
                    self.messageboxerror("Возникли проблемы с соединением с базой данной код 1004")
            else:
                self.pInput1.engineer_combo.setCurrentIndex(0)
            if self.pProjects.getProjectsIdFromDB():
                self.page.setCurrentIndex(1)
    def on_deleted_Clicked(self):
        id = self.pProjects.projects[self.pProjects.ind][2]
        if (DataManager.delete('Project', str(id))):
            print("Удален проект " + str(id))
            self.pProjects.getProjectsIdFromDB()
    def on_selectionChanged(self, selected):
        for i in selected.indexes():
            self.pProjects.ind = int(i.row())
            self.pProjects.butOpenProj.setIcon(QIcon("icon/OpenFile.png"))
            self.pOutput.id = int(self.pProjects.projects[self.pProjects.ind][2])
    def butNewProj_Clicked(self):
        if self.pOutput.createInDBProject():
            self.page.setCurrentIndex(2)
    def butLeft1_Clicked(self):
        self.page.setCurrentIndex(1)
        # очистить первую страницу ввода данных
        self.pInput1.inCompany.clear()
        self.pInput1.inBush.clear()
        self.pInput1.inWell.clear()
        self.pInput1.inField.clear()
        self.pInput1.inCompanyINN.clear()
        # очистить вторую страницу ввода данных
        self.pInput2.inInnerDiam.clear()
        self.pInput2.inOuterDiam.clear()

    def updatePrIn(self):
        if ((DataManager.update('Project', 'Company', PrIn.Company, self.id)) and
            (DataManager.update('Project', 'Field', PrIn.Field, self.id)) and
            (DataManager.update('Project', 'Bush', PrIn.Bush, self.id)) and
            (DataManager.update('Project', 'Well', PrIn.Well, self.id)) and
            (DataManager.update('Project', 'Date', PrIn.Date, self.id)) and
            (DataManager.update('Project', 'Engineer', PrIn.Engineer, self.id))):
            return True
        else:
            self.messageboxerror("Проблема с подключением к базе данных код 1011")

    def butNext1_Clicked(self):
        if (validateStr(self.pInput1.inCompany.text(), 30)
                and validateStr(self.pInput1.inField.text(), 30)
                and validateStr(self.pInput1.inPhoneNumber.text(), 100)
                and validateStr(self.pInput1.inBush.text(), 30)
                and validateStr(self.pInput1.inWell.text(), 30)):
            self.messageboxerror("Поля пусты или переполнены(не более 30 знаков)")
            return
        PrIn.Company = self.pInput1.inCompany.text()
        PrIn.Field = self.pInput1.inField.text()
        selectDate = self.pInput1.inData.date()
        PrIn.Date = selectDate.toString(Qt.ISODate)
        PrIn.Bush = self.pInput1.inBush.text()
        PrIn.Well = self.pInput1.inWell.text()
        PrIn.ContactEngineer = self.pInput1.inPhoneNumber.text()
        self.id = self.pOutput.id
        engineer = DataManager.select_users_where("id", "name='" + self.pInput1.engineer_combo.currentText() + "'")
        if engineer:
            PrIn.Engineer = str(engineer[0][0])
            self.updatePrIn()
            self.page.setCurrentIndex(3)
        else:
            self.messageboxerror("Проблема с подключением к базе данных код 1012")


    def butLeft2_Clicked(self):
        self.page.setCurrentIndex(2)


    def checkdiametr(self, OD = HoIn.DiameterExternal, ID = HoIn.DiameterInterior):
        if OD < ID:
            self.messageboxerror("Наружный диаметр меньше внутреннего")
        else:
            self.pOutput.tab = "Images"

    def saveHoIn(self):
        HoIn.WellBottomProjMD = int(self.pInput2.inDownhole11.text())
        HoIn.WellBottomProjTVD = int(self.pInput2.inDownhole12.text())
        HoIn.WellBottomFactMD = int(self.pInput2.inDownhole21.text())
        HoIn.WellBottomFactTVD = int(self.pInput2.inDownhole22.text())
        HoIn.OpenHoleDiameter = int(self.pInput2.inDiamOpenBarrel.text())
        HoIn.OffsetVertical = int(self.pInput2.inOffsetFromVert.text())
        HoIn.OpenHoleLenght = int(self.pInput2.inLenBarrel.text())
        HoIn.MaxAngle = int(self.pInput2.inCorner.text())
        HoIn.MaxAngleInterval = int(self.pInput2.inInterval.text())
        HoIn.HoleType = self.pInput2.inTypeWell.currentText()
        HoIn.ReservoirPressure = int(self.pInput2.inReservoirPres.text())
        HoIn.WellheadPressure = int(self.pInput2.inWellHeadPres.text())
        HoIn.LinerRunningInterval = self.pInput2.inDesInterShank.text()
        HoIn.DescentDepth = int(self.pInput2.inDescentDepth.text())
        HoIn.CKODdepth = int(self.pInput2.inDepthCCODE.text())

    def updateHoIn(self):
        DataManager.update('Project', 'TypeWell', HoIn.HoleType, self.id)
        DataManager.update('Project', 'Downhole11', HoIn.WellBottomProjMD, self.id)
        DataManager.update('Project', 'Downhole12', HoIn.WellBottomProjTVD, self.id)
        DataManager.update('Project', 'Downhole21', HoIn.WellBottomFactMD, self.id)
        DataManager.update('Project', 'Downhole22', HoIn.WellBottomFactTVD, self.id)
        DataManager.update('Project', 'DiamOpenBarrel', HoIn.OpenHoleDiameter, self.id)
        DataManager.update('Project', 'OffsetFromVert', HoIn.OffsetVertical, self.id)
        DataManager.update('Project', 'LenBarrel', HoIn.OpenHoleLenght, self.id)
        DataManager.update('Project', 'Corner', HoIn.MaxAngle, self.id)
        DataManager.update('Project', 'Interval', HoIn.MaxAngleInterval, self.id)
        DataManager.update('Project', 'ReservoirPres', HoIn.ReservoirPressure, self.id)
        DataManager.update('Project', 'WellHeadPres', HoIn.WellheadPressure, self.id)
        DataManager.update('Project', 'DesInterShank', HoIn.LinerRunningInterval, self.id)
        DataManager.update('Project', 'DescentDepth', HoIn.DescentDepth, self.id)
        DataManager.update('Project', 'DepthCCODE', HoIn.CKODdepth, self.id)

    def butNext2_Clicked(self):
        if (validateInt(self.pInput2.inDownhole11.text())
                and validateInt(self.pInput2.inDownhole12.text())
                and validateInt(self.pInput2.inDownhole21.text())
                and validateInt(self.pInput2.inDownhole22.text())
                and validateInt(self.pInput2.inDiamOpenBarrel.text())
                and validateInt(self.pInput2.inOffsetFromVert.text())
                and validateInt(self.pInput2.inLenBarrel.text())
                and validateInt(self.pInput2.inCorner.text())
                and validateInt(self.pInput2.inInterval.text())
                and validateInt(self.pInput2.inReservoirPres.text())
                and validateInt(self.pInput2.inWellHeadPres.text())
                and validateInt(self.pInput2.inDesInterShank.text())
                and validateFloat(self.pInput2.inOuterDiam.text())
                and validateFloat(self.pInput2.inInnerDiam.text())
                and validateInt(self.pInput2.inDescentDepth.text())
                and validateInt(self.pInput2.inDepthCCODE.text())):
            self.messageboxerror("Поля пусты или имеют недопустимые значения")
            return
        HoIn.NumberOfStagesGRP = int(self.pInput2.inNumberStages.text())
        try:
            if HoIn.NumberOfStagesGRP > 70:
                self.messageboxerror("Введенное кол-во стадий превышено")
                return
        except BaseException:
            self.messageboxerror("Неверное значение")
            return
        self.saveHoIn()
        HoIn.DiameterExternal = round(float(self.pInput2.inOuterDiam.text()))
        HoIn.DiameterInterior = round(float(self.pInput2.inInnerDiam.text()))
        HoIn.CompositionType = self.pInput2.compon_combo.currentText()
        self.checkdiametr(HoIn.DiameterExternal, HoIn.DiameterInterior)
        self.pOutput.countDetails = HoIn.NumberOfStagesGRP * 2 + 7
        """
        отправление данных в базу данных
        """
        self.updateHoIn()
        DataManager.update('Project', 'OuterDiam', str(HoIn.DiameterExternal), self.id)
        DataManager.update('Project', 'InnerDiam', str(HoIn.DiameterInterior), self.id)
        DataManager.sql_query("UPDATE Project SET NumberStages='" + str(HoIn.NumberOfStagesGRP) + "' WHERE id='" + str(self.id) + "';")
        DataManager.sql_query("UPDATE Project SET TypeComp='" + str(HoIn.CompositionType) + "' WHERE id='" + str(self.id) + "';")
        self.pOutput.getProjectFromDB()
        tab = self.pOutput.tab
        self.pOutput.drawsBD()
        self.pOutput.drawProject(PrIn, HoIn)
        self.pOutput.butLeft.hide()
        self.pOutput.butLeftCreateProject.show()
        self.page.setCurrentIndex(4)

    def butOpenProj_Clicked(self):
        if (self.pProjects.ind != -1):
            self.pOutput.butLeft.show()
            self.pOutput.butLeftCreateProject.hide()
            self.pOutput.getProjectFromDB()
            self.pOutput.drawProject()
            self.page.setCurrentIndex(4)
        else:
            QMessageBox.critical(self, "Ошибка", "Проект не выбран", QMessageBox.Ok)

    def LeftOpenProject(self):
        self.pInput1.cleanPage()
        self.pInput2.cleanPage()
        self.pProjects.getProjectsIdFromDB()
        self.pOutput.butLeftCreateProject.hide()
        self.pOutput.CleanPage()
        self.page.setCurrentIndex(1)


    def resizeEvent(self, event):
        self.resized.emit()
        return super(TextEditDemo, self).resizeEvent(event)


    def openSheme(self):
        self.page.setCurrentIndex(5)
        self.pBigSheme.details = self.pOutput.bigdet
        self.pBigSheme.index = self.pOutput.girik
        self.pBigSheme.setImage(self.pOutput.bigdet)
    def closeSheme(self):
        self.page.setCurrentIndex(4)

    def searchImageonSheme(self):
        try:
            if (len(self.pBigSheme.details) != 0):
                self.pBigSheme.index = int(self.pBigSheme.Number.text()) - 1
                self.pBigSheme.setImage(self.pOutput.bigdet)
        except:
            pass

    def ClearLayout(self):
        self.pOutput.images = []

    def DynamicSize(self):
        koefW = self.size().width() / 1100
        koefH = self.size().height() / 550
        self.pAuthorization.DynamicSize(koefW, koefH)
        self.pProjects.DynamicSize(koefW, koefH)
        self.pInput1.DynamicSize(koefW, koefH)
        self.pInput2.DynamicSize(koefW, koefH)
        self.pOutput.DynamicSize(koefW, koefH)
        self.pBigSheme.DynamicSize(koefW, koefH)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TextEditDemo()
    win.show()
    sys.exit(app.exec_())

