from PyQt5.QtWidgets import (QPushButton, QListWidget, QLineEdit, QFrame, QLabel, QMainWindow, QApplication, QAbstractItemView)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QSize
import sys

#В этом классе описывается основной графический интерфейс пользователя
class MainUI(QMainWindow):
    def __init__(self):
        super().__init()


    def initUI(self):
        rec = QApplication.desktop()
        rec = rec.screenGeometry()
        self.screenWidth, self.screenHeight = rec.width(), rec.height()
        
        top_field_width = 0.173 * self.screenWidth
        top_field_height = 0.037 * self.screenHeight
        
        if sys.platform == 'linux':
            font = QFont("Libaration Serif")
        else:
            font = QFont("Calibri")
        
        
        self.framepal = QPalette()
        self.framepal.setColor(self.backgroundRole(), QColor(240, 240, 240)) 
 
        self.topframe = QFrame(self)
        self.topframe.setFrameShape(QFrame.StyledPanel)
        self.topframe.setPalette(self.framepal)
        self.topframe.setAutoFillBackground(True)
        self.topframe.resize(0.307 * self.screenWidth, 0.22 * self.screenHeight)
        self.topframe.move(0.01 * self.screenWidth, 0.037 * self.screenHeight)
        
        self.lbl1 = QLabel('Enter poject name : ', self.topframe)
        font.setPixelSize(28 / 1920 * self.screenWidth)
        self.lbl1.setFont(font)
        self.lbl1.move(10 / 1920 * self.screenWidth, 15 / 1080 * self.screenHeight)
        
        self.le = QLineEdit(self.topframe)
        self.le.resize(top_field_width, top_field_height)
        self.le.move(243 / 1920 * self.screenWidth, 16 / 1080 * self.screenHeight)
        font.setPixelSize(26 / 1920 * self.screenWidth)
        self.le.setFont(font)
        
        self.srclbl = QLabel('Source code file : ', self.topframe)
        font.setPixelSize(28 / 1920 * self.screenWidth)
        self.srclbl.setFont(font)
        self.srclbl.move(10 / 1920 * self.screenWidth, 75 / 1080 * self.screenHeight)
        
        self.lt = QListWidget(self.topframe)
        self.lt.resize(top_field_width, top_field_height)
        self.lt.move(243 / 1920 * self.screenWidth, 74 / 1080 * self.screenHeight)
        font.setPixelSize(24 / 1920 * self.screenWidth)
        self.lt.setFont(font)
        self.lt.setIconSize(QSize(25 / 1080 * self.screenHeight, 25 / 1080 * self.screenHeight))
        self.lt.setContextMenuPolicy(Qt.CustomContextMenu)
        
        self.lbln = QLabel('Build target folder : ', self.topframe)
        font.setPixelSize(28 / 1920 * self.screenWidth)
        self.lbln.setFont(font)
        self.lbln.move(10 / 1920 * self.screenWidth, 133 / 1080 * self.screenHeight)
        
        self.folle = QLineEdit(self.topframe)
        self.folle.resize(top_field_width, top_field_height)
        self.folle.move(243 / 1920 * self.screenWidth, 134 / 1080 * self.screenHeight)
        font.setPixelSize(25 / 1920 * self.screenWidth)
        self.folle.setFont(font)
        self.folle.setReadOnly(True)
        
        self.choosebtn = QPushButton('Choose file', self.topframe)
        self.choosebtn.move(10 / 1920 * self.screenWidth, 185 / 1080 * self.screenHeight)
        self.choosebtn.resize(0.07 * self.screenWidth, 0.037 * self.screenHeight)
        font.setPixelSize(22 / 1920 * self.screenWidth)
        self.choosebtn.setFont(font)
        
        self.choosefoldbtn = QPushButton('Choose folder', self.topframe)
        self.choosefoldbtn.move(155 / 1920 * self.screenWidth, 185 / 1080 * self.screenHeight)
        self.choosefoldbtn.resize(0.07 * self.screenWidth, 0.037 * self.screenHeight)
        font.setPixelSize(22 / 1920 * self.screenWidth)
        self.choosefoldbtn.setFont(font)
        
        #self.warnlbl = QLabel('                                                                    ', self.topframe)
        #self.warnlbl.setFont(QFont('Calibri', 14))
        #self.warnlbl.move(294 / 1920 * self.screenWidth, 190 / 1080 * self.screenHeight)
        #self.warnlbl.setStyleSheet("QLabel { color : red; }")
        
        self.leftframe = QFrame(self)
        self.leftframe.setFrameShape(QFrame.StyledPanel)
        self.leftframe.setPalette(self.framepal)
        self.leftframe.setAutoFillBackground(True)
        self.leftframe.resize(0.106 * self.screenWidth, 0.351 * self.screenHeight)
        self.leftframe.move(20 / 1920 * self.screenWidth, 290 / 1080 * self.screenHeight)
        
        self.lbl2 = QLabel('Build tool : ', self.leftframe)
        font.setPixelSize(27 / 1920 * self.screenWidth)
        self.lbl2.setFont(font)
        self.lbl2.move(10 / 1920 * self.screenWidth, 15 / 1080 * self.screenHeight)
        
        self.toolle = QLineEdit(self.leftframe)
        self.toolle.resize(182 / 1920 * self.screenWidth, 37 / 1080 * self.screenHeight)
        self.toolle.move(10 / 1920 * self.screenWidth, 60 / 1080 * self.screenHeight)
        font.setPixelSize(26 / 1920 * self.screenWidth)
        self.toolle.setFont(font)
        self.toolle.setReadOnly(True)
        
        self.settingsbtn = QPushButton('Settings', self.leftframe)
        self.settingsbtn.move(30 / 1920 * self.screenWidth, 115 / 1080 * self.screenHeight)
        self.settingsbtn.resize(140 / 1920 * self.screenWidth, 45 / 1080 * self.screenHeight)
        font.setPixelSize(23 / 1920 * self.screenWidth)
        self.settingsbtn.setFont(font)
        
        self.buildbtn = QPushButton('Build', self.leftframe)
        self.buildbtn.move(17 / 1920 * self.screenWidth, 311 / 1080 * self.screenHeight)
        self.buildbtn.resize(170 / 1920 * self.screenWidth, 50 / 1080 * self.screenHeight)
        font.setPixelSize(25 / 1920 * self.screenWidth)
        self.buildbtn.setFont(font)
        
        self.rightframe = QFrame(self)
        self.rightframe.setFrameShape(QFrame.StyledPanel)
        self.rightframe.setPalette(self.framepal)
        self.rightframe.setAutoFillBackground(True)
        self.rightframe.resize(0.192 * self.screenWidth, 0.351 * self.screenHeight)
        self.rightframe.move(240 / 1920 * self.screenWidth, 290 / 1080 * self.screenHeight)
        
        self.list = QListWidget(self.rightframe)
        self.list.resize(350 / 1920 * self.screenWidth, 250 / 1080 * self.screenHeight)
        self.list.move(9 / 1920 * self.screenWidth, 46 / 1080 * self.screenHeight)
        self.list.setIconSize(QSize(27 / 1080 * self.screenHeight, 27 / 1080 * self.screenHeight))
        font.setPixelSize(23 / 1920 * self.screenWidth)
        self.list.setFont(font)
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
        #self.list.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        
        self.lbl4 = QLabel('Include files : ', self.rightframe)
        self.lbl4.move(10 / 1920 * self.screenWidth, 5 / 1080 * self.screenHeight)
        font.setPixelSize(26 / 1920 * self.screenWidth)
        self.lbl4.setFont(font)
        
        self.addbtn = QPushButton('Add', self.rightframe)
        self.addbtn.move(8 / 1920 * self.screenWidth, 315 / 1080 * self.screenHeight)
        self.addbtn.resize(135 / 1920 * self.screenWidth, 46 / 1080 * self.screenHeight)
        font.setPixelSize(23 / 1920 * self.screenWidth)
        self.addbtn.setFont(font)
        
        self.delbtn = QPushButton('Remove', self.rightframe)
        self.delbtn.move(225 / 1920 * self.screenWidth, 315 / 1080 * self.screenHeight)
        self.delbtn.resize(135  / 1920 * self.screenWidth, 46 / 1080 * self.screenHeight)
        font.setPixelSize(23 / 1920 * self.screenWidth)
        self.delbtn.setFont(font)
    
        
        
        
        
        
