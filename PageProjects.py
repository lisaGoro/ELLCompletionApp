from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QFont, QPainter, QColor, QBrush
from PyQt5.Qt import *
import DataManager
from datetime import datetime
import random
import resourses

name = ""
class PageProjects(QWidget):


    def __init__(self, parent=None):
        super().__init__()
        fontIdB = QFontDatabase.addApplicationFont("Fonts/helvetica_bold.otf")
        Helvetica_Bold = QFontDatabase.applicationFontFamilies(fontIdB)[0]
        fontIdR = QFontDatabase.addApplicationFont("Fonts/helvetica_regular.otf")
        Helvetica_Regular = QFontDatabase.applicationFontFamilies(fontIdR)[0]
        shadow = QGraphicsDropShadowEffect(self,
                                           blurRadius=35,
                                           color=QColor(0, 0, 0, 35),
                                           offset=QPointF(10, 10),
                                           )
        self.setGraphicsEffect(shadow)
        self.projects = []
        self.ind = -1
        self.koefH = 1
        self.koefW = 1
        self.name = ""
        self.access = "nothing"
        self.iduser = 1

        self.lwelcome = QLabel(self)
        self.lwelcome.setText(setWelcome())
        self.lwelcome.resize(600, 50)
        self.lwelcome.setAlignment(Qt.AlignCenter)
        self.lwelcome.setStyleSheet("color: White")
        self.lwelcome.move(250, 0)
        self.lwelcome.setFont(QFont(Helvetica_Bold, 14))

        self.lwelcomename = QLabel(self)
        self.lwelcomename.resize(600, 50)
        self.lwelcomename.setAlignment(Qt.AlignCenter)
        self.lwelcomename.setStyleSheet("color: White")
        self.lwelcomename.move(250, 20)
        self.lwelcomename.setFont(QFont(Helvetica_Bold, 14))


        self.lUProgects = QLabel(self)
        self.lUProgects.setText("ваши проекты:")
        self.lUProgects.resize(300, 50)
        self.lUProgects.move(400, 40)
        self.lUProgects.setStyleSheet("color: White")
        self.lUProgects.setAlignment(Qt.AlignCenter)
        self.lUProgects.setFont(QFont(Helvetica_Regular, 12))

        self.butOpenProj = QPushButton(self)
        self.butOpenProj.move(245, 395)
        self.butOpenProj.setIcon(QIcon("icon/OpenFileInactive.png"))
        self.butOpenProj.resize(70, 70)
        self.butOpenProj.setIconSize(QSize(70, 70))
        self.butOpenProj.setToolTip("Открыть проект")

        self.butNewProj = QPushButton(self)
        self.butNewProj.move(425, 395)
        self.butNewProj.setIcon(QIcon("icon/NewFile.png"))
        self.butNewProj.resize(70, 70)
        self.butNewProj.setIconSize(QSize(70, 70))
        self.butNewProj.setToolTip("Создать новый проект")

        self.butDelProj = QPushButton(self)
        self.butDelProj.move(605, 395)
        self.butDelProj.setIcon(QIcon("icon/Delete.png"))
        self.butDelProj.resize(70, 70)
        self.butDelProj.setIconSize(QSize(70, 70))
        self.butDelProj.setToolTip("Удалить проект")

        self.butLeft = QPushButton(self)
        self.butLeft.move(785, 395)
        self.butLeft.resize(70, 70)
        self.butLeft.setIcon(QIcon("icon/Exit.png"))
        self.butLeft.setIconSize(QSize(70, 70))
        self.butLeft.setToolTip("Выход")

        """
        список проектов
        """
        self.tableProjects = QTableWidget(self)
        self.tableProjects.resize(700, 300)
        self.tableProjects.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableProjects.move(200, 100)
        self.tableProjects.setColumnCount(1)
        self.tableProjects.verticalHeader().hide()
        self.tableProjects.horizontalHeader().hide()
        self.tableProjects.setColumnWidth(0, self.tableProjects.width())
        self.tableProjects.setEditTriggers(QAbstractItemView.NoEditTriggers)
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
        qp.drawRoundedRect(int(190 * self.koefW), int(75 * self.koefH), int(720 * self.koefW), int(350 * self.koefH), 10, 10)   # Рисование прямоугольника


    def messageboxerror(self, text):
        msg = QMessageBox.critical(self, "Ошибка ", text, QMessageBox.Ok)
        return False

    def getProjectsIdFromDB(self):
        match self.access:
            case "all":
                self.projects = DataManager.select_projects_all()
            case "anything":
                self.projects = DataManager.select_projects_anything(str(self.iduser))
        if self.projects:
            row = len(self.projects)
            self.tableProjects.setRowCount(row)
            self.tableProjects.setSelectionMode(QAbstractItemView.SingleSelection)
            for i in range(row):
                self.tableProjects.setItem(i, 0, QTableWidgetItem(str(self.projects[i][0]) + " " + str(self.projects[i][1])))
            return True
        else:
            self.messageboxerror("Возникли проблемы с соединением с базой данной")


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
                match(str(i.__class__)):
                    case("<class 'PyQt5.QtWidgets.QPushButton'>"):
                        i.setIconSize(i.size())
            except:
                print("Dynamic size missed " + str(i))
        #for i in range (self.tableProjects.rowCount()):
            #self.tableProjects.setRowHeight(i, int(50 * koefH))
        self.tableProjects.setColumnWidth(0, int(self.tableProjects.width()))

def setWelcome():
    hournow = int(datetime.now().hour.real)
    Night = ["Доброй ночи, ", "Рады видеть вас, ", "Рабочий день давно окончен, но", "Бессоница - страшное дело", "Звезды сегодня яркие,"]
    Morning = ["Доброе утро, ", "Рады видеть вас, ", "Надеемся, день пройдет продуктивно, "]
    Day = ["Добрый день, ", "Рады видеть вас, "]
    Evening = ["Добрый вечер, ", "Рады видеть вас, "]
    if hournow < 6:
        return Night[int(random.random() * len(Night))]
    elif hournow < 12:
        return Morning[int(random.random() * len(Morning))]
    elif hournow < 18:
        return Day[int(random.random() * len(Day))]
    else:
        return Evening[int(random.random() * len(Evening))]
