from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import QDir
from utilities.message import Message
from utilities.idleOpener import IdleOpener
from ui.settingsUI import SettingsUI
import pickle
import os
import os.path
import sys

#Окно настроек компилятора
class Settings(SettingsUI):
    def __init__(self, leToChange, projDir):
        super().__init__()
        
        #корректное отображение на линуксе получаемых через QFileDialog путей
        if sys.platform == 'linux' or sys.platform == 'darwin':
            self.filepathStrNum = 13
        else:
            self.filepathStrNum = 0
        
        # Текстовое поле для отображения настроек в главном окне
        self.le = leToChange
        #Флаг для открытия QFileDialog в предыдущей директории при повторном использовании
        self.firstOpen = True
        
        self.projectDir = projDir
        
        self.getBuilders()
        self.initUI(self.builders)
        
        self.ok.clicked.connect(self.okay)
        self.cancel.clicked.connect(self.done)
        self.bldbox.activated[str].connect(self.changeBuilder)
        self.choosebtn.clicked.connect(self.chooseSetupFile)
        self.createbtn.clicked.connect(self.createSetupFile)
        self.editbtn.clicked.connect(self.openSetupInIDLE)
        
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
        startDir = os.getcwd() #После работы необходимо будет вернуться в директорию, в которой мы находились на моменты вызова метода
        try:
            os.chdir(os.path.join(self.projectDir, 'tmp'))
            
            if "setup.py" in os.listdir(os.getcwd()):
                os.chdir(startDir)
                Message.warningMessage(self, " ", "Setup file is already created")
                return
            
            with open('setup.py', 'w') as _:
                pass
        
            self.cxbldle.setText(os.path.join(os.getcwd(), 'setup.py'))
        
            self.openSetupInIDLE()
            os.chdir(startDir) #Возврат в стартовую директорию
        except Exception:
            os.chdir(startDir)
        
        
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
            f = open(os.path.join('data', 'build_settings.pkl'), 'rb')
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
        with open(os.path.join('data', 'builders.pkl'), 'rb') as f:
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
                Message.warningMessage(self, ' ', 'Setup file must be .py')
            else:
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
            
            with open(os.path.join('data', 'build_settings.pkl'), 'wb') as fl:
                info = ['PyInstaller', str(self.instbldle.text())]
                pickle.dump(info, fl)
                
            self.done(0)
                
        elif str(self.bldbox.currentText()) == 'cx_Freeze':
            path = str(self.cxbldle.text())
            
            if not path or path.isspace():
                Message.warningMessage(self, ' ', 'You have to specify setup file')
            else:
                self.le.setText('cx_Freeze')
                with open(os.path.join('data', 'build_settings.pkl'), 'wb') as fl:
                    info = ['cx_Freeze', path]
                    pickle.dump(info, fl)
                    
                self.done(0)
                
        else:        
            self.done(0)
                
        
        
            
            