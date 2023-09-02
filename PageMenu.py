from PyQt5.QtWidgets import *
from PyQt5.Qt import *
class PageMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        #self.layer = QVBoxLayout(self)

        #self.layer.setAlignment(Qt.AlignCenter)

        self.butCreateS = QPushButton('Составить схему', self)
        self.butCreateS.move(375, 100)
        self.butCreateS.resize(200, 50)

        #self.layer.addWidget(self.butCreateS)

        self.butBaseProj = QPushButton('База проектов', self)
        self.butBaseProj.move(375, 200)
        self.butBaseProj.resize(200, 50)

        self.butBaseComp = QPushButton('База компоновок', self)
        self.butBaseComp.move(375, 300)
        self.butBaseComp.resize(200, 50)
        self.butCreateS.height()
        #self.layer.addWidget(self.butCreateS)
        #self.layer.addWidget(self.butBaseComp)
        #self.layer.addWidget(self.butBaseProj)

        #self.butCreateS.StyleSheet = '''
        
            #background-color: #2196f3;
        
        #'''
        self.SetNormalSize()

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