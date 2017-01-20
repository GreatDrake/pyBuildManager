from PyQt5.QtWidgets import QListWidgetItem, QFileDialog, QAction, QMenu, qApp
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, QSize, QPoint, QDir
from utilities.builder import Builder
from utilities.message import Message
from utilities.idleOpener import IdleOpener
from ui.mainUI import MainUI
from aboutDialog import About
from settingsWindow import Settings
import os
import os.path
import shutil
import pickle
import webbrowser
import sys


class Window(MainUI):
    def __init__(self):
        #Вызываем метод __init__ базового класса QMainWindow
        super().__init__()
        #Инициализируем весь интерфейс из класса MainUI
        MainUI.initUI(self)
        
        #Для открытия папки в файловом менеджере ОС
        self.folderToOpen = None
        
        #Флаг для открытия QFileDialog в предыдущей директории при повторном использовании
        self.firstOpen = True
        
        #корректное отображение на линуксе получаемых через QFileDialog путей
        if sys.platform == 'linux' or sys.platform == 'darwin': # -19(-13) linux filepathStrNum
            self.filepathStrNum = 13
        else:
            self.filepathStrNum = 0
        
        self.projectDir = os.getcwd() 
        
        self.resourceFolder = os.path.join(self.projectDir, "Resources")
        
        self.source = None #source - файл с исходным кодом 
        
        #Иконки к возможным расширениям файлов
        self.extensions = {'.py'  : os.path.join(self.resourceFolder, 'pyt.png' ),  '.txt'  : os.path.join(self.resourceFolder, 'text.png'),
                           '.png' : os.path.join(self.resourceFolder, 'png.png' ),  '.jpg'  : os.path.join(self.resourceFolder, 'jpg.png' ),
                           '.dll' : os.path.join(self.resourceFolder, 'dll.png' ),  '.html' : os.path.join(self.resourceFolder, 'html.png'),
                           '.htm' : os.path.join(self.resourceFolder, 'html.png'),  '.pyc'  : os.path.join(self.resourceFolder, 'pyt.png' ),
                           '.rar' : os.path.join(self.resourceFolder, 'rar.png' ),  '.zip'  : os.path.join(self.resourceFolder, 'zip.png' ),
                           '.ico' : os.path.join(self.resourceFolder, 'ico.png' ),  '.psd'  : os.path.join(self.resourceFolder, 'psd.png' ),
                           '.pyd' : os.path.join(self.resourceFolder, 'pyt.png' ),  '.pyw'  : os.path.join(self.resourceFolder, 'pyt.png' ),
                           '.pdf' : os.path.join(self.resourceFolder, 'pdf.png' ),  '.exe'  : os.path.join(self.resourceFolder, 'exe.png' ),
                           '.css' : os.path.join(self.resourceFolder, 'css.png' ),  '.qss'  : os.path.join(self.resourceFolder, 'css.png' ),
                           '.gif' : os.path.join(self.resourceFolder, 'gif.png' ),  '.js'   : os.path.join(self.resourceFolder, 'js.png'  ),
                           '.xml' : os.path.join(self.resourceFolder, 'xml.png')
                           }
        
        #Создание временной папки с проектом
        try:
            os.mkdir('tmp')
        except Exception:
            shutil.rmtree('tmp', ignore_errors=True)
            os.mkdir('tmp')
        
        shutil.rmtree('tmp2', ignore_errors=True)
        
        #удаление временного файла лог компиляции
        try:
            os.remove(os.path.join(self.projectDir, 'temporaryfilelogtodel.txt'))
        except Exception:
            pass
        
        self.initBuilders()
        
        self.initUI()
        
        
    # Поиск установленных инструментов компиляции
    def initBuilders(self):
        self.builders = []
            
        try:
            import PyInstaller
            self.builders.append('PyInstaller')
        except ImportError:
            pass
        else:
            del PyInstaller
            
        try:
            import cx_Freeze
            self.builders.append('cx_Freeze')
        except ImportError:
            pass
        else:
            del cx_Freeze
            
        try:
            import py2exe
            self.builders.append('py2exe')
        except ImportError:
            pass
        else:
            del py2exe
            
        with open(os.path.join('data', 'builders.pickle'), 'wb') as fl: # В builders.pickle находятся названия доступных инструментов компиляции
            pickle.dump(self.builders, fl)
            
            
        if self.builders:
            with open(os.path.join('data', 'build_settings.pickle'), 'wb') as fl: # В build_settings.pickle находится информация вида
                pickle.dump([self.builders[0], ''], fl)                           # [(Название инструмента), (дополнительная информация)]    
        else:                                                                     # доп. информация - модификаторы компиляции или путь к setup файлу или
            try:
                os.remove(os.path.join('data', 'build_settings.pickle'))
            except Exception:
                pass
            
        
    def initUI(self):
        self.addAct = QAction('&Add file', self)
        self.addAct.triggered.connect(self.addFile)
        
        self.delAct = QAction('&Delete', self)
        self.delAct.triggered.connect(self.delete)
        
        self.addFolderAction = QAction('Add folder', self)
        self.addFolderAction.triggered.connect(self.addFolder)
        
        self.idleAction = QAction("&Edit with IDLE", self)
        self.idleAction.triggered.connect(self.openSourceInIDLE)
        
        self.exitAction = QAction(QIcon(os.path.join("Resources", "exit.png")), "&Exit", self)
        self.exitAction.triggered.connect(self.quitApplication)
        self.exitAction.setShortcut("Ctrl+Q")
        
        self.buildAction = QAction(QIcon(os.path.join("Resources", "build.png")), "&Build", self)
        self.buildAction.triggered.connect(self.build)
        self.buildAction.setShortcut("Ctrl+B")
        
        self.aboutAction = QAction(QIcon(os.path.join("Resources", "question.png")), "&About", self)
        self.aboutAction.triggered.connect(self.showAboutDialog)
        
        self.manualAction = QAction(QIcon(os.path.join("Resources", "manual.png")), "&Manual", self)
        self.manualAction.triggered.connect(self.showManual)
        
        self.openAction = QAction("&Open in file manager", self)
        self.openAction.triggered.connect(self.openFolderInExplorer)
        
        self.openIncludesAction = QAction("&Open this folder", self)
        self.openIncludesAction.triggered.connect(self.openIncludesFolderInExplorer)
        
        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.buildAction)
        fileMenu.addAction(self.exitAction)
        
        helpMenu = menubar.addMenu("&Help")
        helpMenu.addAction(self.aboutAction)
        helpMenu.addAction(self.manualAction)
        
        self.choosebtn.clicked.connect(self.addSourceFile)
        self.choosefoldbtn.clicked.connect(self.addSourceFolder)
        self.buildbtn.clicked.connect(self.build)
        self.list.customContextMenuRequested[QPoint].connect(self.onContext)
        self.addbtn.clicked.connect(self.addFile)
        self.delbtn.clicked.connect(self.delete)
        self.settingsbtn.clicked.connect(self.showSettings)
        self.lt.customContextMenuRequested[QPoint].connect(self.onTopContext)
        
        pal = self.palette()
        role = self.backgroundRole()
        pal.setColor(role, QColor(252, 252, 252)) #QColor(255, 252, 221)
        
        self.setFixedSize(630 / 1920 * self.screenWidth, 690 / 1080 * self.screenHeight)
        self.setWindowTitle('pyBuildManager') 
        self.setWindowIcon(QIcon(os.path.join(self.resourceFolder, 'pyic.ico')))
        self.setPalette(pal)
        self.show()

        
    def closeEvent(self, event):
        self.quitApplication()
        event.accept()

        
    def quitApplication(self):
        #Перед выходом необходимо удалить временную папку с проектом
        shutil.rmtree(os.path.join(self.projectDir, 'tmp'), ignore_errors=True)
        shutil.rmtree(os.path.join(self.projectDir, 'tmp2'), ignore_errors=True)
        try:
            os.remove(os.path.join(self.projectDir, 'temporaryfilelogtodel.txt'))
        except Exception:
            pass
        qApp.quit()


    def showAboutDialog(self):
        about = About()
        about.setWindowFlags(Qt.Window)
        self.centerDialog(about)
        about.exec_()
        
        
    def showSettings(self):
        settings = Settings(self.toolle, self.projectDir)
        settings.setWindowFlags(Qt.Widget)
        self.centerDialog(settings)
        settings.exec_()
        
        
    def centerDialog(self, dialog):
        x, y = (self.x(), self.y())
        x += self.width() / 2 - dialog.width() / 2
        y += self.height() / 2 - dialog.height() / 2
        dialog.move(x, y)
        
        
    def showManual(self):
        webbrowser.open(os.path.join('Manual', 'manual.html'))
        
        
    #Вызов пользователем контекстного меню у QListWidget   
    def onContext(self, pos):
        item = self.list.itemAt(pos)
        menu = QMenu("&Menu", self)
        if item: #Пользователь кликнул по элементу
            if hasattr(item, 'folderpath'):
                menu.addAction(self.openAction)
                self.folderToOpen = item.folderpath
            menu.addAction(self.delAct)
        
        else: #Пользователь кликнул по пустому пространству QListWidget
            menu.addAction(self.addAct)
            menu.addAction(self.addFolderAction)
            menu.addAction(self.openIncludesAction)
        
        menu.exec_(self.list.mapToGlobal(pos))
        
        
    #Вызов контекстного меню у QListWidget в верхней рамке
    def onTopContext(self, pos):
        item = self.lt.itemAt(pos)
        
        if item:
            menu = QMenu("&Menu", self)
            menu.addAction(self.idleAction)
        
            menu.exec_(self.lt.mapToGlobal(pos))
    
    #Открытиe папки в файловом менеджере os         
    def explorerOpen(self, folder):
        try:
            if sys.platform == 'linux':
                os.system('xdg-open "%s"' % folder)
            elif sys.platform == 'darwin':
                os.system('open "%s"' % folder)
            elif sys.platform == 'win32':
                os.startfile(folder)
        except Exception:
            pass
           
           
    def openFolderInExplorer(self):
        if self.folderToOpen:
            self.explorerOpen(self.folderToOpen)
            
            
    def openIncludesFolderInExplorer(self):
        folder = os.path.join(self.projectDir, "tmp")
        self.explorerOpen(folder)     
    
    
    #Открыть файл с исходным кодом в IDLE        
    def openSourceInIDLE(self):
        if hasattr(self, "fullsource"):
            IdleOpener.openInIdle(self, self.fullsource)
                
                                
    #Компиляция проекта
    def build(self):
        missing = []
        
        if (self.le.text() == '') or (self.le.text().isspace()):
            missing.append("Project name")
            
        if (self.source is None):
            missing.append("Source file")
        
        if not hasattr(self, 'folder'): #folder - папка в которую нужно будет перенести скомпилированный проект
            missing.append("Target folder")
            
        if (not self.toolle.text()):
            missing.append("Build tool")
            
        if any(missing):
            warning_text = 'You have to specify:\n'
            for i in range(len(missing)-1):
                warning_text += missing[i] + '\n'
                
            warning_text += missing[-1]
            
            Message.warningMessage(self, ' ', warning_text)
            return
        
        src = os.path.join(self.projectDir, 'tmp')
        build_info = None
        btns_to_disable = [self.buildbtn, self.settingsbtn, self.choosebtn, self.choosefoldbtn, 
                           self.addbtn, self.delbtn]
            
        try:
            f = open(os.path.join('data', 'build_settings.pickle'), 'rb')
            build_info = pickle.load(f)
            f.close()
        except Exception:
            try:
                f.close()
            except Exception:
                pass
            
        try:
            shutil.copyfile(self.fullsource, os.path.join('tmp', self.source)) # Повторно скопировать файл с исходным кодом в папку с проектом
            pass                                                               # на случай его изменения
        except Exception:
            pass
        
         
        if build_info:
            if build_info[0] == 'PyInstaller':
                
                Builder.pyinstaller_build(source_name=self.source, source_folder=src, working_dir=self.projectDir, 
                                          project_name=self.le.text(), build_target=self.folder, includes_folder=src, 
                                          build_options=build_info[1], buttons_to_disable=btns_to_disable, cur_self=self)
            
            elif build_info[0] == 'cx_Freeze':
                
                Builder.cxfreeze_build(source_name=self.source, source_folder=src, working_dir=self.projectDir, 
                                       project_name=self.le.text(), build_target=self.folder, includes_folder=src,
                                       setup_file=build_info[1], buttons_to_disable=btns_to_disable, cur_self=self)
            else:
                pass
        
        
    #Удаление включаемого файла или папки из QListWidget и из папки с проектом   
    def delete(self):
        listitems = self.list.selectedItems()
        
        if not listitems:
            return
        for item in listitems:
            #Удаление элементов QListWidget а также файлов и папок
            try:
                os.remove(os.path.join('tmp', str(item.text())))
            except Exception:
                shutil.rmtree(os.path.join('tmp', str(item.text())))
            self.list.takeItem(self.list.row(item))
            

    #Добавление включаемого файла в папку с проетом и в QListWidget       
    def addFile(self):
        dial = QFileDialog()

        #Получение нужного для добавления файла
        try:
            if self.firstOpen:
                name = dial.getOpenFileName(self, "Choose file", QDir.homePath())
                self.firstOpen = False
            else:
                name = dial.getOpenFileName(self, "Choose file")
            file = str(name)[2:-6-self.filepathStrNum]  #('C:/Users/Nikita/Desktop/spiral iz chiesl.py', '')
            file = file.replace('/', os.path.sep)
            parts = file.split(os.path.sep)
            shutil.copyfile(file, os.path.join('tmp', parts[-1])) #parts[-1] Собственно имя файла
        except Exception:
            dial.accept()
            return 

        #Получение нужной иконки исходя из расширения файла
        ext = '.' + parts[-1].split('.')[-1]
        ext = ext.lower()
        try:
            iconpath = self.extensions[ext]
        except Exception:
            iconpath = os.path.join(self.resourceFolder, 'blank.png')
        
        a = QListWidgetItem(parts[-1])
        a.setIcon(QIcon(iconpath))
        a.setSizeHint(QSize(100 / 1920 * self.screenWidth, 33 / 1080 * self.screenHeight))
        self.list.addItem(a)
        

    #Выбор файла с исходным кодом для компиляции   
    def addSourceFile(self):
        #Т.к. файл с исходным кодом может быть лишь один, нужно удалить выбранный
        #чтобы выбрать новый
        if self.lt.count() != 0:
            item = self.lt.item(0)
            os.remove(os.path.join('tmp', str(item.text())))
            self.lt.takeItem(self.lt.row(item))
        
        dial = QFileDialog()

        #Получение нужного для добавления файла
        try:
            if self.firstOpen:
                name = dial.getOpenFileName(self, "Choose file", QDir.homePath()) 
                self.firstOpen = False
            else:
                name = dial.getOpenFileName(self, "Choose file") 
            file = str(name)[2:-6-self.filepathStrNum]  #('C:/Users/Nikita/Desktop/spiral iz chiesl.py', '')
            file = file.replace('/', os.path.sep)
            parts = file.split(os.path.sep)
            self.fullsource = file
            if not (('.py' in parts[-1]) or ('pyw' in parts[-1])): #Проверка верности расширения файла
                if file:
                    #self.warnlbl.setText('Source file must be .py or .pyw')
                    Message.warningMessage(self, ' ', 'Source file must be .py')

                self.source = None
                
                return
            shutil.copyfile(file, os.path.join('tmp', parts[-1])) #parts[-1] Собственно имя файла
        except Exception:
            dial.accept()
            return
        else:
            self.source = parts[-1]
            #self.warnlbl.setText('                                                                    ')

        #Получение нужной иконки исходя из расширения файла
        ext = '.' + parts[-1].split('.')[1]
        try:
            iconpath = self.extensions[ext]
        except Exception:
            iconpath = os.path.join(self.resourceFolder, 'blank.ico')
        
        a = QListWidgetItem(parts[-1])
        a.setIcon(QIcon(iconpath))
        a.setSizeHint(QSize(100 / 1920 * self.screenWidth, 35 / 1080 * self.screenHeight))
        a.setFlags(a.flags() and Qt.ItemIsEnabled)
        self.lt.addItem(a)
        

    #Добавление включаемой папки в папку с проектом и в QListWidget    
    def addFolder(self):
        dial = QFileDialog()
        
        try:
            if self.firstOpen:
                name = dial.getExistingDirectory(self, "Choose folder", QDir.homePath())
                self.firstOpen = False
            else: 
                name = dial.getExistingDirectory(self, "Choose folder")
            fold = os.path.basename(name)
            folpath = os.getcwd()
            shutil.copytree(name, os.path.join('tmp', fold))
            folpath = os.path.join(folpath, 'tmp', fold)
        except Exception:
            dial.accept()
            return
        
        a = QListWidgetItem(fold)
        a.setIcon(QIcon(os.path.join('Resources','folder.png')))
        a.setSizeHint(QSize(100 / 1920 * self.screenWidth, 33 / 1080 * self.screenHeight))
        a.__dict__['folderpath'] = folpath
        self.list.addItem(a)
        

    #Выбор папки в которую будет помещена папка с готовым проектом  
    def addSourceFolder(self):
        dial = QFileDialog()
        
        fold = None
        
        try:
            if self.firstOpen:
                name = dial.getExistingDirectory(self, "Choose folder", QDir.homePath())
                self.firstOpen = False
            else:
                name = dial.getExistingDirectory(self, "Choose folder")
            fold = str(name)
        except Exception:
            dial.accept()
            return
        
        if fold:
            self.folder = fold
            self.folle.setText(self.folder)
        


    
        
