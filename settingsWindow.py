from PyQt5.QtWidgets import QDialog, QLabel, QApplication, QComboBox, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import QDir
from message import Message
from idleOpener import IdleOpener
import pickle
import os
import os.path
import sys

#Окно настроек компилятора
class Settings(QDialog):
    def __init__(self, leToChange, projDir):
        super().__init__()
        
        #Флаг для открытия QFileDialog в предыдущей директории при повторном использовании
        self.firstOpen = True
        
        #корректное отображение на линуксе получаемых через QFileDialog путей
        if sys.platform == 'linux' or sys.platform == 'darwin':
            self.filepathStrNum = 13
        else:
            self.filepathStrNum = 0
        
        # Текстовое поле для отображения настроек в главном окне
        self.le = leToChange
        
        self.projectDir = projDir
        
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
        self.ok.resize(100 / 1920 * self.screenWidth, 34 / 1080 * self.screenHeight)
        font.setPixelSize(22 / 1920 * self.screenWidth)
        self.ok.setFont(font)
        self.ok.clicked.connect(self.okay)
        
        self.cancel = QPushButton('Cancel', self)
        self.cancel.move(20 / 1920 * self.screenWidth, 225 / 1080 * self.screenHeight)
        self.cancel.resize(100 / 1920 * self.screenWidth, 34 / 1080 * self.screenHeight)
        font.setPixelSize(22 / 1920 * self.screenWidth)
        self.cancel.setFont(font)
        self.cancel.clicked.connect(self.done)
        
        self.lbl = QLabel("Build tool : ", self)
        font.setPixelSize(28 / 1920 * self.screenWidth)
        self.lbl.setFont(font)
        self.lbl.move(60 / 1920 * self.screenWidth, 20 / 1080 * self.screenHeight) 
        self.lbl.font().setPixelSize(10)
        
        self.getBuilders()
        
        self.bldbox = QComboBox(self)
        self.bldbox.addItems(self.builders)
        self.bldbox.resize(150 / 1920 * self.screenWidth, 34 / 1080 * self.screenHeight)
        self.bldbox.move(190 / 1920 * self.screenWidth, 23 / 1080 * self.screenHeight)
        font.setPixelSize(22 / 1920 * self.screenWidth)
        self.bldbox.setFont(font)
        self.bldbox.activated[str].connect(self.changeBuilder)
        
        
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
        self.choosebtn.clicked.connect(self.chooseSetupFile)
        self.choosebtn.hide()
        
        self.createbtn = QPushButton("Create", self)
        self.createbtn.move(225 / 1920 * self.screenWidth, 98 / 1080 * self.screenHeight)
        self.createbtn.resize(86 / 1920 * self.screenWidth, 32 / 1080 * self.screenHeight)
        font.setPixelSize(22 / 1920 * self.screenWidth)
        self.createbtn.setFont(font)
        self.createbtn.clicked.connect(self.createSetupFile)
        self.createbtn.hide()
        
        self.editbtn = QPushButton("Edit", self)
        self.editbtn.move(133 / 1920 * self.screenWidth, 98 / 1080 * self.screenHeight)
        self.editbtn.resize(86 / 1920 * self.screenWidth, 32 / 1080 * self.screenHeight)
        font.setPixelSize(22 / 1920 * self.screenWidth)
        self.editbtn.setFont(font)
        self.editbtn.clicked.connect(self.openSetupInIDLE)
        self.editbtn.hide()
        
        self.cxbldle = QLineEdit(self)
        self.cxbldle.move(10 / 1920 * self.screenWidth, 145 / 1080 * self.screenHeight)
        self.cxbldle.resize(395 / 1920 * self.screenWidth, 37 / 1080 * self.screenHeight)
        font.setPixelSize(23 / 1920 * self.screenWidth)
        self.cxbldle.setFont(font)
        self.cxbldle.setReadOnly(True)
        self.cxbldle.hide()
        
        #self.warnlbl = QLabel("                                                                         ", self) #"Setup file must be .py"
        #self.warnlbl.adjustSize()
        #self.warnlbl.setStyleSheet("QLabel { color : red; }")
        #self.warnlbl.setFont(QFont("Calibri", 14))
        #self.warnlbl.move(10 / 1920 * self.screenWidth, 185 / 1080 * self.screenHeight)
        #self.warnlbl.hide()
        
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
        
        
        self.initSettings()
        
        pal = self.palette()
        role = self.backgroundRole()
        pal.setColor(role, QColor(248, 248, 248))
        
        self.setFixedSize(415 / 1920 * self.screenWidth, 285 / 1080 * self.screenHeight)
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon(os.path.join("Resources", "settings.png")))
        self.setPalette(pal)
        self.show()
    
    #Создать setup файл    
    def createSetupFile(self):
        curdir = os.getcwd() #После работы необходимо будет вернуться в директорию, в которой мы находились на моменты вызова метода
        try:
            os.chdir(os.path.join(self.projectDir, 'tmp'))
        
            with open('setup.py', 'w') as _:
                pass
        
            self.cxbldle.setText(os.path.join(os.getcwd(), 'setup.py'))
        
            self.openSetupInIDLE()
            os.chdir(curdir) #Возврат в стартовую директорию
        except Exception:
            os.chdir(curdir)
        
        
    #Открыть setup файл в IDLE        
    def openSetupInIDLE(self):
        self.fullsource = self.cxbldle.text() #Путь к setup файлу
        if not self.fullsource or self.fullsource.isspace():
            return
        
        IdleOpener.openInIdle(self, self.fullsource)
     
     
    #Отобразить уже выбранные настройки если таковые имеются    
    def initSettings(self):
        settings = None
        
        try:
            f = open(os.path.join('data', 'build_settings.pickle'), 'rb')
            settings = pickle.load(f)
            f.close()
        except Exception:
            try:
                f.close()
            except Exception:
                pass
          
        if not settings:
            if str(self.bldbox.currentText()):
                settings = [str(self.bldbox.currentText()), '']
            else:
                settings = ['', '']
            
        if settings[0] == 'cx_Freeze':
            self.bldbox.setCurrentIndex(self.freezeIndex)
            self.showFreezeUI()
            self.cxbldle.setText(settings[1])
            
        elif settings[0] == 'PyInstaller':
            self.bldbox.setCurrentIndex(self.installerIndex)
            self.showInstallerUI()
            self.instbldle.setText(settings[1])
    
    
    #Получение доступных инструментов компиляции    
    def getBuilders(self):
        with open(os.path.join('data', 'builders.pickle'), 'rb') as f:
            self.builders = pickle.load(f)
            
        if 'PyInstaller' in self.builders:
            self.installerIndex = self.builders.index('PyInstaller')
            
        if 'cx_Freeze' in self.builders:
            self.freezeIndex = self.builders.index('cx_Freeze')
            
        if 'py2exe' in self.builders:
            self.py2exeIndex = self.builders.index('py2exe')
        
      
    #Выбор инструмента компиляции пользователем        
    def changeBuilder(self, s):
        if s == 'cx_Freeze':
            self.showFreezeUI()
        elif s == 'PyInstaller':
            self.showInstallerUI()
      
    #Отобразить интерфейс для PyInstaller  
    def showInstallerUI(self):
        self.lbl3.show()
        self.instbldle.show()
        
        self.lbl2.hide()
        self.choosebtn.hide()
        self.createbtn.hide()
        self.editbtn.hide()
        self.cxbldle.hide()
        #self.warnlbl.hide()
    
    #Отобразить интерфейс для cx_Freeze
    def showFreezeUI(self):
        self.lbl3.hide()
        self.instbldle.hide()
        
        self.lbl2.show()
        self.choosebtn.show()
        self.createbtn.show()
        self.editbtn.show()
        self.cxbldle.show()
        #self.warnlbl.show()
        
    
    #Выбор setup файла для cx_Freeze 
    def chooseSetupFile(self):
        dial = QFileDialog()
        file = None
        
        try:
            if self.firstOpen:
                name = dial.getOpenFileName(self, 'Choose file', QDir.homePath())
                self.firstOpen = False
            else:
                name = dial.getOpenFileName(self, 'Choose file')
            file = str(name)[2:-6-self.filepathStrNum]  #('C:/Users/Nikita/Desktop/spiral iz chiesl.py', '')
            file = file.replace('/', os.path.sep)
        except Exception:
            dial.accept()
            return
        
        if file:
            if os.path.basename(file).split('.')[1] != 'py':
                #self.warnlbl.setText("Setup file must be .py")
                #self.warnlbl.adjustSize()
                Message.warningMessage(self, ' ', 'Setup file must be .py')
            else:
                #self.warnlbl.setText("                                                                                                 ")
                #self.warnlbl.adjustSize()
                self.cxbldle.setText(file)
        
        
    #Выход без сохранения настроек
    def closeEvent(self, event):
        event.accept()
        
        
    #Выход с сохранением настроек
    def okay(self):
        if str(self.bldbox.currentText()) == 'PyInstaller':
            curdir = os.getcwd()
        
            #удаляем setup файл если он остался после работы с cx_Freeze
            try:
                os.chdir(os.path.join(self.projectDir, 'tmp')) 
                os.remove('setup.py')
                os.chdir(curdir)
            except Exception:
                os.chdir(curdir)
            
            self.le.setText('PyInstaller')
            
            with open(os.path.join('data', 'build_settings.pickle'), 'wb') as fl:
                info = ['PyInstaller', str(self.instbldle.text())]
                pickle.dump(info, fl)
                
            self.done(0)
                
        elif str(self.bldbox.currentText()) == 'cx_Freeze':
            path = str(self.cxbldle.text())
            
            if not path or path.isspace():
                #self.warnlbl.setText('You have to specify setup file')
                #self.warnlbl.adjustSize()
                Message.warningMessage(self, ' ', 'You have to specify setup file')
            else:
                self.le.setText('cx_Freeze')
                with open(os.path.join('data', 'build_settings.pickle'), 'wb') as fl:
                    info = ['cx_Freeze', path]
                    pickle.dump(info, fl)
                    
                self.done(0)
                
        else:        
            self.done(0)
                
        
        
            
            