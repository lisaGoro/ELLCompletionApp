from PyQt5.QtWidgets import *
from PyQt5.Qt import *
import DataManager
import subprocess

class BigSheme(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.index = 0
        self.details = []
        self.tab = ""
        self.label = QLabel(self)
        self.label.resize(100, 500)
        self.label.move(450, 0)
        self.label.setAlignment(Qt.AlignCenter)


        self.Number = QLabel(self)
        self.Number.setText("0")
        self.Number.move(70, 450)
        self.Number.resize(30, 19)


        self.name = QLabel(self)
        self.name.move(500, 50)
        self.name.resize(1200, 20)

        self.number = QLabel(self)
        self.number.move(500, 70)
        self.number.resize(1200, 20)

        self.length = QLabel(self)
        self.length.move(500, 160)
        self.length.resize(1200, 20)

        self.OD = QLabel(self)
        self.OD.move(500, 140)
        self.OD.resize(1200, 20)

        self.ID = QLabel(self)
        self.ID.move(500, 120)
        self.ID.resize(1200, 20)

        self.passporthref = QPushButton("открыть паспорт", self)
        self.passporthref.move(500, 180)
        self.passporthref.resize(120, 20)


        self.lanotherdetails = QLabel(self)
        self.lanotherdetails.move(500, 220)
        self.lanotherdetails.resize(1200, 20)
        self.lanotherdetails.setText("Похожие:")
        self.anotherdetails = QLabel(self)
        self.anotherdetails.move(500, 240)
        self.anotherdetails.resize(1200, 20)


        self.NextBut = QPushButton(">", self)
        self.NextBut.resize(52, 530)
        self.NextBut.move(1020, 0)


        self.BackBut = QPushButton("<", self)
        self.BackBut.resize(50, 470)
        self.BackBut.move(0, 60)


        self.BackBackBut = QPushButton("<<", self)
        self.BackBackBut.resize(50, 50)
        self.BackBackBut.move(0, 0)

        # События
        self.NextBut.clicked.connect(self.nextImg)
        self.BackBut.clicked.connect(self.backImg)
        self.passporthref.clicked.connect(self.openpassportinbrowser)

        self.SetNormalSize()

    def searchAnotherDetails(self, number):
        details = DataManager.select_details(number[0:3])
        if details:
            details = details[1:len(details)]
            for i in range(len(details)):
                details[i] = details[i][2:3]
        return details

    def openpassportinbrowser(self):
        path = str(self.details[self.index][7])
        if path != None:
            subprocess.Popen([path], shell=True)



    def setImage(self, details):
        img = QPixmap(details[self.index][3])
        self.label.setPixmap(img.scaled(100, 400, Qt.KeepAspectRatio, Qt.FastTransformation))
        self.label.move(350, 10)
        self.name.setText(details[self.index][1])
        self.number.setText(details[self.index][2])
        self.ID.setText("Наружный диаметр: " + str(details[self.index][4]) + " мм")
        self.OD.setText("Внутренний диаметр: " + str(details[self.index][5]) + " мм")
        self.length.setText("Длина: " + str(details[self.index][6]) + " мм")
        self.anotherdetails.setText(str(self.searchAnotherDetails(details[self.index][2])))
        self.Number.setText("" + str(details[self.index][0]))

    def nextImg(self):
        if (self.index < len(self.details) - 1):
            self.index += 1
            self.setImage(self.details)

    def backImg(self):
        if (self.index > 0 and self.index < len(self.details) + 1):
            self.index -= 1
            self.setImage(self.details)


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