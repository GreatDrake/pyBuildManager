from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QDialog, QApplication, QComboBox
from PyQt5.QtGui import QFont
import sys

#В этом классе описывается основной графический интерфейс пользователя
class SettingsUI(QDialog):
    def __init__(self):
        super().__init__()
        
    def initUI(self, builders):
        rec = QApplication.desktop()
        rec = rec.screenGeometry()
        self.screenWidth, self.screenHeight = rec.width(), rec.height()
        
        if sys.platform == 'linux':
            font = QFont("Liberation Serif")
        elif sys.platform == 'darwin':
            font = QFont("Times")
        else:
            font = QFont("Calibri")
        
        self.ok = QPushButton('OK', self)
        self.ok.move(295 / 1920 * self.screenWidth, 225 / 1080 * self.screenHeight)
        self.ok.resize(100 / 1920 * self.screenWidth, 33 / 1080 * self.screenHeight)
        font.setPixelSize(22 / 1920 * self.screenWidth)
        self.ok.setFont(font)
       
        self.cancel = QPushButton('Cancel', self)
        self.cancel.move(20 / 1920 * self.screenWidth, 225 / 1080 * self.screenHeight)
        self.cancel.resize(100 / 1920 * self.screenWidth, 33 / 1080 * self.screenHeight)
        font.setPixelSize(22 / 1920 * self.screenWidth)
        self.cancel.setFont(font)
        
        self.lbl = QLabel("Build tool : ", self)
        font.setPixelSize(28 / 1920 * self.screenWidth)
        self.lbl.setFont(font)
        self.lbl.move(65 / 1920 * self.screenWidth, 20 / 1080 * self.screenHeight) 
        self.lbl.font().setPixelSize(10)
         
        self.bldbox = QComboBox(self)
        self.bldbox.addItems(builders)
        self.bldbox.resize(140 / 1920 * self.screenWidth, 32 / 1080 * self.screenHeight)
        self.bldbox.move(195 / 1920 * self.screenWidth, 24 / 1080 * self.screenHeight)
        font.setPixelSize(22 / 1920 * self.screenWidth)
        self.bldbox.setFont(font)
        
        
        # cx_Freeze UI  ##############################################################################   
        ############################################################################################## 
          
        self.lbl2 = QLabel("Setup file : ", self)
        font.setPixelSize(26 / 1920 * self.screenWidth)
        self.lbl2.setFont(font)
        self.lbl2.move(10 / 1920 * self.screenWidth, 96 / 1080 * self.screenHeight) 
        self.lbl2.hide()
        
        self.choosebtn = QPushButton('Choose', self)
        self.choosebtn.move(317 / 1920 * self.screenWidth, 98 / 1080 * self.screenHeight)
        self.choosebtn.resize(86 / 1920 * self.screenWidth, 32 / 1080 * self.screenHeight)
        font.setPixelSize(22 / 1920 * self.screenWidth)
        self.choosebtn.setFont(font)
        self.choosebtn.hide()
        
        self.createbtn = QPushButton("Create", self)
        self.createbtn.move(225 / 1920 * self.screenWidth, 98 / 1080 * self.screenHeight)
        self.createbtn.resize(86 / 1920 * self.screenWidth, 32 / 1080 * self.screenHeight)
        font.setPixelSize(22 / 1920 * self.screenWidth)
        self.createbtn.setFont(font)
        self.createbtn.hide()
        
        self.editbtn = QPushButton("Edit", self)
        self.editbtn.move(133 / 1920 * self.screenWidth, 98 / 1080 * self.screenHeight)
        self.editbtn.resize(86 / 1920 * self.screenWidth, 32 / 1080 * self.screenHeight)
        font.setPixelSize(22 / 1920 * self.screenWidth)
        self.editbtn.setFont(font)
        self.editbtn.hide()
        
        self.cxbldle = QLineEdit(self)
        self.cxbldle.move(10 / 1920 * self.screenWidth, 145 / 1080 * self.screenHeight)
        self.cxbldle.resize(395 / 1920 * self.screenWidth, 37 / 1080 * self.screenHeight)
        font.setPixelSize(23 / 1920 * self.screenWidth)
        self.cxbldle.setFont(font)
        self.cxbldle.setReadOnly(True)
        self.cxbldle.hide()
        
        ############################################################################################## 
        ############################################################################################## 
        
        
        # PyInstaller UI ############################################################################# 
        ############################################################################################## 
        
        self.lbl3 = QLabel("Build options : ", self)
        font.setPixelSize(26 / 1920 * self.screenWidth)
        self.lbl3.setFont(font)
        self.lbl3.move(10 / 1920 * self.screenWidth, 95 / 1080 * self.screenHeight) 
        self.lbl3.hide()
        
        self.instbldle = QLineEdit(self)
        self.instbldle.move(10 / 1920 * self.screenWidth, 145 / 1080 * self.screenHeight)
        self.instbldle.resize(395 / 1920 * self.screenWidth, 37 / 1080 * self.screenHeight)
        font.setPixelSize(23 / 1920 * self.screenWidth)
        self.instbldle.setFont(font)
        self.instbldle.hide()
        self.instbldle.setPlaceholderText('For example: --noconsole, or leave empty')
        
        ############################################################################################## 
        ############################################################################################## 
        
        
    #Отобразить интерфейс для PyInstaller  
    def showInstallerUI(self):
        self.lbl3.show()
        self.instbldle.show()
        
        self.lbl2.hide()
        self.choosebtn.hide()
        self.createbtn.hide()
        self.editbtn.hide()
        self.cxbldle.hide()
        
        self.ok.show()
        self.cancel.show()
        
    
    #Отобразить интерфейс для cx_Freeze
    def showFreezeUI(self):
        self.lbl3.hide()
        self.instbldle.hide()
        
        self.lbl2.show()
        self.choosebtn.show()
        self.createbtn.show()
        self.editbtn.show()
        self.cxbldle.show()
        
        self.ok.show()
        self.cancel.show()
     
    #Отобразить интерфейс для py2exe 
    def showPy2ExeUi(self):
        self.lbl2.hide()
        self.choosebtn.hide()
        self.createbtn.hide()
        self.editbtn.hide()
        self.cxbldle.hide()
        
        self.lbl3.hide()
        self.instbldle.hide()
        
        self.ok.hide()
        self.cancel.hide()
       
        
        
        
        