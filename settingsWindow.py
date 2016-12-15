from PyQt5.QtWidgets import QDialog, QLabel, QApplication, QComboBox, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import QDir
from message import Message
import pickle
import os
import sys
import subprocess

#Окно настроек компилятора
class Settings(QDialog):
    def __init__(self, leToChange, projDir):
        super().__init__()
        
        #корректное отображение на линуксе получаемых через QFileDialog путей
        if sys.platform == 'linux':
            self.strnum = 13
        else:
            self.strnum = 0
        
        # Текстовое поле для отображения настроек в главном окне
        self.le = leToChange
        
        self.projectDir = projDir
        
        rec = QApplication.desktop()
        rec = rec.screenGeometry()
        self.screen_width, self.screen_height = rec.width(), rec.height()
        
        self.ok = QPushButton('OK', self)
        self.ok.move(295 / 1920 * self.screen_width, 225 / 1080 * self.screen_height)
        self.ok.resize(100 / 1920 * self.screen_width, 34 / 1080 * self.screen_height)
        self.ok.setFont(QFont('Calibri Bold', 11 / 1080 * self.screen_height))
        self.ok.clicked.connect(self.okay)
        
        self.cancel = QPushButton('Cancel', self)
        self.cancel.move(20 / 1920 * self.screen_width, 225 / 1080 * self.screen_height)
        self.cancel.resize(100 / 1920 * self.screen_width, 34 / 1080 * self.screen_height)
        self.cancel.setFont(QFont('Calibri Bold', 11 / 1080 * self.screen_height))
        self.cancel.clicked.connect(self.done)
        
        
        self.lbl = QLabel("Build tool : ", self)
        self.lbl.setFont(QFont("Calibri", 17 / 1920 * self.screen_width))
        self.lbl.move(60 / 1920 * self.screen_width, 20 / 1080 * self.screen_height) 
        
        self.getBuilders()
        
        self.bldbox = QComboBox(self)
        self.bldbox.addItems(self.builders)
        self.bldbox.resize(150 / 1920 * self.screen_width, 34 / 1080 * self.screen_height)
        self.bldbox.move(190 / 1920 * self.screen_width, 23 / 1080 * self.screen_height)
        self.bldbox.setFont(QFont('Calibri', 13))
        self.bldbox.activated[str].connect(self.changeBuilder)
        
        
        # cx_Freeze UI  ##############################################################################   
        ############################################################################################## 
          
        self.lbl2 = QLabel("Setup file : ", self)
        self.lbl2.setFont(QFont("Calibri", 16 / 1920 * self.screen_width))
        self.lbl2.move(10 / 1920 * self.screen_width, 95 / 1080 * self.screen_height) 
        self.lbl2.hide()
        
        self.choosbtn = QPushButton('Choose', self)
        self.choosbtn.move(317 / 1920 * self.screen_width, 98 / 1080 * self.screen_height)
        self.choosbtn.resize(86 / 1920 * self.screen_width, 32 / 1080 * self.screen_height)
        self.choosbtn.setFont(QFont('Calibri', 13 / 1080 * self.screen_height))
        self.choosbtn.clicked.connect(self.chooseSetupFile)
        self.choosbtn.hide()
        
        self.createbtn = QPushButton("Create", self)
        self.createbtn.move(226 / 1920 * self.screen_width, 98 / 1080 * self.screen_height)
        self.createbtn.resize(86 / 1920 * self.screen_width, 32 / 1080 * self.screen_height)
        self.createbtn.setFont(QFont('Calibri', 13 / 1080 * self.screen_height))
        self.createbtn.clicked.connect(self.createSetupFile)
        self.createbtn.hide()
        
        self.editbtn = QPushButton("Edit", self)
        self.editbtn.move(135 / 1920 * self.screen_width, 98 / 1080 * self.screen_height)
        self.editbtn.resize(86 / 1920 * self.screen_width, 32 / 1080 * self.screen_height)
        self.editbtn.setFont(QFont('Calibri', 13 / 1080 * self.screen_height))
        self.editbtn.clicked.connect(self.openSetupInIDLE)
        self.editbtn.hide()
        
        self.cxbldle = QLineEdit(self)
        self.cxbldle.move(10 / 1920 * self.screen_width, 145 / 1080 * self.screen_height)
        self.cxbldle.resize(395 / 1920 * self.screen_width, 37 / 1080 * self.screen_height)
        self.cxbldle.setFont(QFont('Calibri', 13 / 1080 * self.screen_height))
        self.cxbldle.setReadOnly(True)
        self.cxbldle.hide()
        
        self.warnlbl = QLabel("                                                                         ", self) #"Setup file must be .py"
        self.warnlbl.adjustSize()
        self.warnlbl.setStyleSheet("QLabel { color : red; }")
        self.warnlbl.setFont(QFont("Calibri", 14 / 1920 * self.screen_width))
        self.warnlbl.move(10 / 1920 * self.screen_width, 185 / 1080 * self.screen_height)
        self.warnlbl.hide()
        
        ############################################################################################## 
        ############################################################################################## 
        
        
        
        # PyInstaller UI ############################################################################# 
        ############################################################################################## 
        
        self.lbl3 = QLabel("Build options : ", self)
        self.lbl3.setFont(QFont("Calibri", 16 / 1920 * self.screen_width))
        self.lbl3.move(10 / 1920 * self.screen_width, 95 / 1080 * self.screen_height) 
        self.lbl3.hide()
        
        self.instbldle = QLineEdit(self)
        self.instbldle.move(10 / 1920 * self.screen_width, 145 / 1080 * self.screen_height)
        self.instbldle.resize(395 / 1920 * self.screen_width, 37 / 1080 * self.screen_height)
        self.instbldle.setFont(QFont('Calibri', 13 / 1080 * self.screen_height))
        self.instbldle.hide()
        self.instbldle.setPlaceholderText('For example: --noconsole, or leave empty')
        
        ############################################################################################## 
        ############################################################################################## 
        
        self.initSettings()
        
        pal = self.palette()
        role = self.backgroundRole()
        pal.setColor(role, QColor(248, 248, 248))
        
        self.setFixedSize(415 / 1920 * self.screen_width, 285 / 1920 * self.screen_width)
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon(os.path.join("Resources", "settings.png")))
        self.setPalette(pal)
        self.show()
        
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
        python = os.path.dirname(sys.executable)
        idle = os.path.join(python, "Lib", "idlelib") #Директория с idle
        fullsource = self.cxbldle.text() #Путь к setup файлу
        
        if os.path.isdir(idle) and fullsource:
            if 'idle.bat' in os.listdir(idle):
                idle = os.path.join(idle, 'idle.bat')
                
                try:
                    if fullsource:
                        command = idle + " " + fullsource
                        command = r'' + command
                        subprocess.Popen(command, shell=True) # Что-то типа:   ...\\idle.bat ...\\setup.py
                        try:
                            subprocess.check_output()
                        except subprocess.CalledProcessError:
                            Message.errorMessage(self, "Fail", "Failed to open IDLE")
                except Exception:
                    pass
                
            elif 'idle.py' in os.listdir(idle):
                idle = os.path.join(idle, 'idle.py')
                
                try:
                    if fullsource:
                        command = idle + " " + fullsource
                        command = r'' + command
                        subprocess.Popen(command, shell=True) # Что-то типа:   ...\\idle.py ...\\setup.py
                        try:
                            subprocess.check_output()
                        except subprocess.CalledProcessError:
                            Message.errorMessage(self, "Fail", "Failed to open IDLE")
                except Exception:
                    pass
            else:
                Message.errorMessage(self, "Fail", "Failed to open IDLE")
        else:
            Message.errorMessage(self, "Fail", "Failed to open IDLE")
     
     
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
        self.choosbtn.hide()
        self.createbtn.hide()
        self.editbtn.hide()
        self.cxbldle.hide()
        self.warnlbl.hide()
    
    #Отобразить интерфейс для cx_Freeze
    def showFreezeUI(self):
        self.lbl3.hide()
        self.instbldle.hide()
        
        self.lbl2.show()
        self.choosbtn.show()
        self.createbtn.show()
        self.editbtn.show()
        self.cxbldle.show()
        self.warnlbl.show()
        
    
    #Выбор setup файла для cx_Freeze 
    def chooseSetupFile(self):
        dial = QFileDialog()
        file = None
        
        try:
            name = dial.getOpenFileName(self, "Choose file", QDir.homePath())
            file = str(name)[2:-6-self.strnum]  #('C:/Users/Nikita/Desktop/spiral iz chiesl.py', '')
            file = file.replace('/', os.path.sep)
        except Exception:
            dial.accept()
            return
        
        if file:
            if os.path.basename(file).split('.')[1] != 'py':
                self.warnlbl.setText("Setup file must be .py")
                self.warnlbl.adjustSize()
            else:
                self.warnlbl.setText("                                                                                                 ")
                self.warnlbl.adjustSize()
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
                self.warnlbl.setText('You have to specify setup file')
                self.warnlbl.adjustSize()
            else:
                self.le.setText('cx_Freeze')
                with open(os.path.join('data', 'build_settings.pickle'), 'wb') as fl:
                    info = ['cx_Freeze', path]
                    pickle.dump(info, fl)
                self.done(0)
                
        else:
            self.done(0)
                
        
        
            
            
            
            
            
            
            
            
            
            