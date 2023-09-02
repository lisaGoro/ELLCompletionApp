import sys
from datetime import datetime
import DataManager
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
import FileCreating
from Data import Data
from PIL import Image, ImageDraw

PrIn = Data.ProjectInfo()
HoIn = Data.HoleInfo()
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

def paintIMGsmall(img):
    return img.scaled(120, 1000, Qt.KeepAspectRatio, Qt.FastTransformation)


class ClickedWid(QWidget):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.clicked.emit()
class ClickedLabel(QLabel):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.clicked.emit()

class PageOutput(QWidget):
    """def dataTake(dataInputnew):
        dataInput = dataInputnew"""
    def __init__(self, parent=None):
        super().__init__()
        self.details = []
        self.bigdet = []
        self.place_img = []
        self.id_project = 2
        self.project = []
        self.id = 2
        self.countDetails = 0
        self.Date = ""
        self.tab = "Images"

        self.saveas = QComboBox(self)
        self.saveas.addItem('Сохранить как...')
        self.saveas.addItem('PDF')
        self.saveas.addItem('XLSX')
        self.saveas.move(800, 20)
        self.saveas.resize(150, 20)

        # Создание поля с картинками
        self.scrollarea = QScrollArea(self)
        self.shemeWid = ClickedWid(self)
        self.schemeLayout = QVBoxLayout(self)
        self.shemeWid.setLayout(self.schemeLayout)
        self.shemeWid.setStyleSheet('.QWidget {background-color: White')
        self.scrollarea.setWidget(self.shemeWid)
        self.scrollarea.setGeometry(0, 0, 150, 450)
        self.scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollarea.move(10, 20)
        self.shemeWid.resize(200, 100)

        # Таблица общая информация
        self.lprojectInfo = QLabel(self)
        self.lprojectInfo.move(230, -10)
        self.lprojectInfo.resize(400, 30)
        self.lprojectInfo.setText('Общая информация')
        self.projectInfo = QTableWidget(self)
        self.projectInfo.setColumnCount(4)
        self.projectInfo.setRowCount(4)
        self.projectInfo.resize(560, 200)
        self.projectInfo.move(230, 20)
        self.projectInfo.setStyleSheet('.QWidget {background-color: White')

        self.projectInfo.setItem(0, 0, QTableWidgetItem("Компания"))
        self.projectInfo.setItem(0, 2, QTableWidgetItem("Месторождение"))
        self.projectInfo.setItem(1, 0, QTableWidgetItem("Скважина"))
        self.projectInfo.setItem(1, 2, QTableWidgetItem("Куст"))
        self.projectInfo.setItem(2, 0, QTableWidgetItem("Инженер"))
        self.projectInfo.setItem(2, 2, QTableWidgetItem("Контакт инженера"))
        self.projectInfo.setItem(3, 0, QTableWidgetItem("Дата подбора"))
        self.projectInfo.setItem(3, 2, QTableWidgetItem("Кол-во стадий ГРП"))
        self.projectInfo.verticalHeader().hide()
        self.projectInfo.horizontalHeader().hide()
        self.projectInfo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.projectInfo.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.projectInfo.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Таблица данные по изделиям
        self.ltable = QLabel(self)
        self.ltable.move(230, 240)
        self.ltable.resize(400, 30)
        self.ltable.setText('Данные по изделиям')
        self.table = QTableWidget(self)
        self.table.move(230, 270)
        self.table.resize(560, 200)
        self.table.verticalHeader().hide()

        # Кнопки для перехода на окно со списком проектов
        self.butLeft = QPushButton('Назад', self)
        self.butLeft.move(10, 500)
        self.butLeft.hide()
        self.butLeftCreateProject = QPushButton('Выйти к списку проектов', self)
        self.butLeftCreateProject.move(820, 450)
        self.butLeftCreateProject.resize(150, 40)
        self.butLeftCreateProject.hide()

        # События
        self.saveas.currentIndexChanged.connect(self.saveasClicked)

        self.SetNormalSize()

    def messageboxerror(self, text):
        msg = QMessageBox.critical(self, "Ошибка ", text, QMessageBox.Ok)
        return False

    def saveasClicked(self):
        match self.saveas.currentText():
            case "PDF":
                FileCreating.nameTable = [self.tab]
                FileCreating.NData = [
                    ('Компания', PrIn.Company, 'Месторождение', PrIn.Field),
                    ('Скважина', PrIn.Well, 'Куст', PrIn.Bush),
                    ('Инженер по подбору', str(PrIn.Engineer), 'Контакт инженера', str(PrIn.ContactEngineer)),
                    ('Дата подбора', PrIn.Date, 'Общая длина компоновки(мм)', '')]
                FileCreating.Data.append(("№", "Название элемента", "Номер элемента", "OD,мм", "ID,мм", "Длина,мм"))
                for i in range(HoIn.NumberOfStagesGRP * 2 + 7):
                    FileCreating.numDetails.append(self.details[i][2])
                    FileCreating.imgDetails.append(self.details[i][3])
                    FileCreating.Data.append((str(self.details[i][0]), self.details[i][1], self.details[i][2], str(self.details[i][4]), str(self.details[i][5]), str(self.details[i][6])))
                FileCreating.NewFile(self, "PDF")
                self.saveas.setCurrentIndex(0)
            case "XLSX":
                FileCreating.NData = ['Компания', 'Месторождение', 'Скважина', 'Куст', 'Инженер по подбору',
                                      'Контакт инженера', 'Дата подбора']
                FileCreating.Data = [PrIn.Company, PrIn.Field, PrIn.Well, PrIn.Bush, PrIn.Engineer, PrIn.ContactEngineer,
                                     PrIn.Date]
                for i in range(HoIn.NumberOfStagesGRP * 2 + 7):
                    FileCreating.numberDetails.append(self.details[i][0])
                    FileCreating.nameDetails.append(self.details[i][1])
                    FileCreating.numDetails.append(self.details[i][2])
                    FileCreating.imgDetails.append(self.details[i][3])
                    FileCreating.OutDiamDetails.append(self.details[i][4])
                    FileCreating.InnDiamDetails.append(self.details[i][5])
                    FileCreating.LengthDetails.append(self.details[i][6])
                FileCreating.NewFile(self, "XLSX")
                self.saveas.setCurrentIndex(0)
            case "Сохранить как...":
                pass


    def QMouseEvent(self, event):
        self.c.closeApp.emit()



    def heightimg(self, img):
        with Image.open(img) as img_1:
            img_1.load()
        h = (img_1.height * 150) // img_1.width
        return h

    # отрисовывает картинки в блоке
    def drawsSheme(self):
        len = 0
        print(self.countDetails)
        for i in range(self.countDetails):
            print(i, len)
            len = len + self.heightimg(self.details[i][3])
        self.shemeWid.resize(200, self.countDetails * 2 + len)
        self.details.reverse()
        for i in range(self.countDetails):
            self.createimg(self.details[i], i)

    def finddetail(self, id_img, place):
        print("SELECT id FROM Images WHERE num='" + id_img + "';")
        id_img = DataManager.sql_query("SELECT id FROM Images WHERE num='" + id_img + "';")
        if id_img:
            self.details.append([place, id_img[0][0]])
        else:
            self.messageboxerror("Проблема с подключением к базе данных код 301")

    def drawsBD(self):
        n = self.countDetails
        self.finddetail("119", 1)
        self.finddetail("120", 2)
        self.finddetail("114", 3)
        self.finddetail("115", 4)
        self.finddetail("113", 5)
        if HoIn.NumberOfStagesGRP > 1:
            for i in range(6, n - 3):
                if i % 2 == 0:
                    self.finddetail("116", i)
                else:
                    self.finddetail("113", i)
        self.finddetail("111", n - 3)
        self.finddetail("117", n - 2)
        self.finddetail("118", n - 1)
        self.finddetail("112", n)
        for i in range(len(self.details)):
            self.saveDetailsInProject(self.details[i][0], self.details[i][1])
        print(self.details)

    def createimg(self, i, inde):
        self.imgnumber = QLabel(self)
        self.imgnumber.setText(str(i[0]))
        with Image.open(i[3]) as img_1:
            img_1.load()
        h = (img_1.height * 150) // img_1.width
        img = QPixmap(i[3]).scaled(150, h)
        self.schemeLayout.label = ClickedLabel('Label')
        self.schemeLayout.label.setToolTip(i[1])
        self.schemeLayout.label.setPixmap(paintIMGsmall(img))
        self.girik = ""
        def giri():
            self.girik = inde
        self.schemeLayout.label.clicked.connect(lambda: giri())
        self.schemeLayout.addWidget(self.imgnumber)
        self.schemeLayout.addWidget(self.schemeLayout.label)

    # Отрисовывает и заполняет таблицу информация по изделиям
    def printProdTable(self):
        self.table.setColumnCount(6)
        self.table.setRowCount(self.countDetails)
        self.table.setHorizontalHeaderLabels(
            ["№", "Название элемента", "Номер", "Внеш диам, мм", "Внут диам, мм", "Длина, мм"])
        for i in range(self.countDetails):
            self.table.setItem(i, 0, QTableWidgetItem(str(self.details[i][0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.details[i][1])))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.details[i][2])))
            self.table.setItem(i, 3, QTableWidgetItem(str(self.details[i][4])))
            self.table.setItem(i, 4, QTableWidgetItem(str(self.details[i][5])))
            self.table.setItem(i, 5, QTableWidgetItem(str(self.details[i][6])))
        self.table.resizeColumnsToContents()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # print("printProdTable")


    # Сохраняет детали в проект в бд
    def saveDetailsInProject(self, place, id_img):
        DataManager.sql_query(
            "INSERT INTO Details (id_img, place, id_project) VALUES (" + str(id_img) + ", " + str(place) + ", " + str(self.id) + ");")
        # print("saveDetailsInProject")

    # Берет все детали проекта с их информацией и изображениями из бд
    def getImagesDetails(self):
        self.details = DataManager.selectseveraltable(
            'Details',
            'Images',
            'Details.place, S.name, S.num, S.href, S.outer_diam, S.inner_diam, S.length, S.passport, Details.cost',
            'Details.id_img = S.id AND Details.id_project = ' + str(self.id))
        self.bigdet = self.details
        # print("getImagesDetails")

    # Берет информацию по проекту из базы данных
    def getProjectFromDB(self):
        self.project = DataManager.select_project_id("Company, Field, Well, Bush, Engineer, Date, NumberStages, TypeComp, OuterDiam, InnerDiam",
                                                     str(self.id))
        if self.project:
            PrIn.Company = self.project[0][0]
            PrIn.Field = self.project[0][1]
            PrIn.Well = self.project[0][2]
            PrIn.Bush = self.project[0][3]
            engineer = DataManager.sql_query("SELECT name FROM users WHERE id='" + str(self.project[0][4]) + "';")
            if engineer:
                PrIn.Engineer = str(engineer[0][0])
            else:
                self.messageboxerror("Возникли проблемы с соединением с базой данных код 405")
            PrIn.ContactEngineer = ""
            PrIn.Date = self.project[0][5]
            HoIn.NumberOfStagesGRP = self.project[0][6]
            HoIn.CompositionType = self.project[0][7]
            HoIn.DiameterExternal = self.project[0][8]
            HoIn.DiameterInterior = self.project[0][9]
        else:
            self.messageboxerror("Возникли проблемы с соединением с базой данной код 404")
        # print("getProjectFromDB")

    # заполняет страницу данными
    def drawProject(self, PrIn = PrIn, HoIn = HoIn):
        """
        таблица общая информация
        """
        self.projectInfo.setItem(0, 1, QTableWidgetItem(PrIn.Company))
        self.projectInfo.setItem(0, 3, QTableWidgetItem(PrIn.Field))
        self.projectInfo.setItem(1, 1, QTableWidgetItem(PrIn.Well))
        self.projectInfo.setItem(1, 3, QTableWidgetItem(PrIn.Bush))
        self.projectInfo.setItem(2, 1, QTableWidgetItem(PrIn.Engineer))
        self.projectInfo.setItem(2, 3, QTableWidgetItem(PrIn.ContactEngineer))
        self.projectInfo.setItem(3, 1, QTableWidgetItem(PrIn.Date))
        self.projectInfo.setItem(3, 3, QTableWidgetItem(str(HoIn.NumberOfStagesGRP)))
        """
        отрисовка изображений
        """
        self.getImagesDetails()
        print("getImagesDetails")
        self.drawsSheme()
        print("drawsSheme")
        self.printProdTable()
        print("printProdTable")
        # print("drawProject")

    # Создает новый проект в бд
    def createInDBProject(self):
        if DataManager.insert('Project', 'Company', '0'):
            self.id = DataManager.selectOne('Project', 'Company', '0', 'id')
            if self.id:
                self.id = str(self.id[0][0])
                return True
            else:
                self.messageboxerror("Проблема с подключением к базе данных код 302")
        else:
            self.messageboxerror("Проблема с подключением к базе данных код 303")
        # print("createInDBProject")

    # Очищает страницу от данных проекта
    def CleanPage(self):
        for i in reversed(range(self.schemeLayout.count())):
            self.schemeLayout.itemAt(i).widget().setParent(None)
        self.details = []
        self.bigdet = []
        # print('clean')

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
        for i in range (5):
            if (i < 5):
                self.projectInfo.setColumnWidth(i, int(self.projectInfo.width() // 4))
            self.projectInfo.setRowHeight(i, self.projectInfo.height() // 5)