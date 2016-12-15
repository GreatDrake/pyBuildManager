from PyQt5.QtWidgets import (QPushButton, QListWidget, QLineEdit, QFrame, QLabel, QMainWindow, QApplication)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QSize

#В этом классе описывается основной графический интерфейс пользователя
class MainUI(QMainWindow):
    def __init__(self):
        super().__init()


    def initUI(self):
        rec = QApplication.desktop()
        rec = rec.screenGeometry()
        self.screen_width, self.screen_height = rec.width(), rec.height()
        
        top_field_width = 0.173 * self.screen_width
        top_field_height = 0.037 * self.screen_height
        width = 0.328 * self.screen_width
        #font_12 = 0.019 * width
        font_14 = 0.022 * width
        font_15 = 0.024 * width
        font_16 = 0.025 * width
        font_17 = 0.027 * width
        

        self.framepal = QPalette()
        self.framepal.setColor(self.backgroundRole(), QColor(240, 240, 240)) #QColor(240, 240, 240)
 

        self.topframe = QFrame(self)
        self.topframe.setFrameShape(QFrame.StyledPanel)
        self.topframe.setPalette(self.framepal)
        self.topframe.setAutoFillBackground(True)
        self.topframe.resize(0.307 * self.screen_width, 0.22 * self.screen_height)
        self.topframe.move(0.01 * self.screen_width, 0.037 * self.screen_height)
        
        self.lbl1 = QLabel('Enter poject name : ', self.topframe)
        self.lbl1.setFont(QFont('Calibri', font_17))
        self.lbl1.move(10 / 1920 * self.screen_width, 15 / 1080 * self.screen_height)
        
        self.le = QLineEdit(self.topframe)
        self.le.resize(top_field_width, top_field_height)
        self.le.move(243 / 1920 * self.screen_width, 16 / 1080 * self.screen_height)
        self.le.setFont(QFont('Calibri', font_15))
        
        self.srclbl = QLabel('Source code file : ', self.topframe)
        self.srclbl.setFont(QFont('Calibri', font_17))
        self.srclbl.move(10 / 1920 * self.screen_width, 75 / 1080 * self.screen_height)
        
        self.lt = QListWidget(self.topframe)
        self.lt.resize(top_field_width, top_field_height)
        self.lt.move(243 / 1920 * self.screen_width, 74 / 1080 * self.screen_height)
        self.lt.setFont(QFont('Calibri', font_15))
        self.lt.setIconSize(QSize(25 / 1080 * self.screen_height, 25 / 1080 * self.screen_height))
        self.lt.setContextMenuPolicy(Qt.CustomContextMenu)
        
        self.lbln = QLabel('Build target folder : ', self.topframe)
        self.lbln.setFont(QFont('Calibri', font_17))
        self.lbln.move(10 / 1920 * self.screen_width, 133 / 1080 * self.screen_height)
        
        self.folle = QLineEdit(self.topframe)
        self.folle.resize(top_field_width, top_field_height)
        self.folle.move(243 / 1920 * self.screen_width, 134 / 1080 * self.screen_height)
        self.folle.setFont(QFont('Calibri', font_15))
        self.folle.setReadOnly(True)
        
        self.choosebtn = QPushButton('Choose file', self.topframe)
        self.choosebtn.move(10 / 1920 * self.screen_width, 185 / 1080 * self.screen_height)
        self.choosebtn.resize(0.07 * self.screen_width, 0.037 * self.screen_height)
        self.choosebtn.setFont(QFont('Calibri', font_14))
        
        self.choosefoldbtn = QPushButton('Choose folder', self.topframe)
        self.choosefoldbtn.move(155 / 1920 * self.screen_width, 185 / 1080 * self.screen_height)
        self.choosefoldbtn.resize(0.07 * self.screen_width, 0.037 * self.screen_height)
        self.choosefoldbtn.setFont(QFont('Calibri', font_14))
        
        self.warnlbl = QLabel('                                                                    ', self.topframe)
        self.warnlbl.setFont(QFont('Calibri', font_14))
        self.warnlbl.move(294 / 1920 * self.screen_width, 190 / 1080 * self.screen_height)
        self.warnlbl.setStyleSheet("QLabel { color : red; }")
        

        self.leftframe = QFrame(self)
        self.leftframe.setFrameShape(QFrame.StyledPanel)
        self.leftframe.setPalette(self.framepal)
        self.leftframe.setAutoFillBackground(True)
        self.leftframe.resize(0.106 * self.screen_width, 0.351 * self.screen_height)
        self.leftframe.move(20 / 1920 * self.screen_width, 290 / 1080 * self.screen_height)
        
        self.lbl2 = QLabel('Build tool : ', self.leftframe)
        self.lbl2.setFont(QFont('Calibri', font_16))
        self.lbl2.move(10 / 1920 * self.screen_width, 15 / 1080 * self.screen_height)
        
        self.toolle = QLineEdit(self.leftframe)
        self.toolle.resize(182 / 1920 * self.screen_width, 37 / 1080 * self.screen_height)
        self.toolle.move(10 / 1920 * self.screen_width, 60 / 1080 * self.screen_height)
        self.toolle.setFont(QFont('Calibri', 14 / 1080 * self.screen_height))
        self.toolle.setReadOnly(True)
        
        self.settingsbtn = QPushButton('Settings', self.leftframe)
        self.settingsbtn.move(30 / 1920 * self.screen_width, 115 / 1080 * self.screen_height)
        self.settingsbtn.resize(140 / 1920 * self.screen_width, 45 / 1080 * self.screen_height)
        self.settingsbtn.setFont(QFont('Calibri', font_14))
        
        
        self.buildbtn = QPushButton('Build', self.leftframe)
        self.buildbtn.move(17 / 1920 * self.screen_width, 311 / 1080 * self.screen_height)
        self.buildbtn.resize(170 / 1920 * self.screen_width, 50 / 1080 * self.screen_height)
        self.buildbtn.setFont(QFont('Calibri', font_15))
        
        self.rightframe = QFrame(self)
        self.rightframe.setFrameShape(QFrame.StyledPanel)
        self.rightframe.setPalette(self.framepal)
        self.rightframe.setAutoFillBackground(True)
        self.rightframe.resize(0.192 * self.screen_width, 0.351 * self.screen_height)
        self.rightframe.move(240 / 1920 * self.screen_width, 290 / 1080 * self.screen_height)
        
        self.list = QListWidget(self.rightframe)
        self.list.resize(350 / 1920 * self.screen_width, 250 / 1080 * self.screen_height)
        self.list.move(9 / 1920 * self.screen_width, 46 / 1080 * self.screen_height)
        self.list.setIconSize(QSize(27 / 1080 * self.screen_height, 27 / 1080 * self.screen_height))
        self.list.setFont(QFont('Calibri', font_15))
        #self.list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        #self.list.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        
        self.lbl4 = QLabel('Include files : ', self.rightframe)
        self.lbl4.move(10 / 1920 * self.screen_width, 5 / 1080 * self.screen_height)
        self.lbl4.setFont(QFont('Calibri', font_15))
        
        self.addbtn = QPushButton('Add', self.rightframe)
        self.addbtn.move(8 / 1920 * self.screen_width, 315 / 1080 * self.screen_height)
        self.addbtn.resize(135 / 1920 * self.screen_width, 46 / 1080 * self.screen_height)
        self.addbtn.setFont(QFont('Calibri', font_14))
        
        self.delbtn = QPushButton('Remove', self.rightframe)
        self.delbtn.move(225 / 1920 * self.screen_width, 315 / 1080 * self.screen_height)
        self.delbtn.resize(135  / 1920 * self.screen_width, 46 / 1080 * self.screen_height)
        self.delbtn.setFont(QFont('Calibri', font_14))
    
        
        
        
        
        
