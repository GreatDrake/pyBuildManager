import shutil
import os
from message import Message
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QMenuBar, QFileDialog, QAction, QApplication, QMessageBox, QPushButton
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QProcess

class BuildLog(QMainWindow):
    def __init__(self, command, callback, projdir, disabled_buttons, args):    
   
        QMainWindow.__init__(self)
        
        rec = QApplication.desktop()
        rec = rec.screenGeometry()
        self.screenWidth, self.screenHeight = rec.width(), rec.height()
        
        self.finished = False
        self.killed = False
        self.box = None
        
        self.args = args
        self.callback = callback
        self.projdir = projdir
        self.disabled_buttons = disabled_buttons
   
        self.edit = QTextEdit(self)
        self.edit.setFont(QFont('Calibri', 12))
        
        self.setCentralWidget(self.edit)
        
        saveAct = QAction(QIcon(os.path.join(self.projdir, 'Resources', 'save.png')),'Save as', self)
        saveAct.triggered.connect(self.saveLog)
        saveAct.setShortcut("Ctrl+S")
        exitAct = QAction(QIcon(os.path.join(self.projdir, 'Resources', 'exit.png')),'Exit', self)
        exitAct.triggered.connect(self.close)
        exitAct.setShortcut("Ctrl+Q")
        menubar = QMenuBar()
        fileMenu = menubar.addMenu("File")
        fileMenu.addAction(saveAct)
        fileMenu.addAction(exitAct)
        self.setMenuBar(menubar)
        
        self.qProcess = QProcess()
        self.qProcess.setProcessChannelMode(QProcess.MergedChannels)   
        self.qProcess.start(command)
        self.qProcess.waitForStarted()
        self.qProcess.readyReadStandardOutput.connect(self.readStdOutput)
        self.qProcess.finished.connect(self.onFinished)
        
        self.setWindowTitle("Build log")
        self.setWindowIcon(QIcon(os.path.join(self.projdir, 'Resources', 'text.png')))
        self.resize(1000 * self.screenWidth / 1920, 800 * self.screenHeight / 1080)
        self.show()
        
    def readStdOutput(self):
        self.edit.append((str(self.qProcess.readAllStandardOutput())[2:-5]).replace('\r\n', ''))
        #self.edit.append('\n')

    def onFinished(self):
        if self.killed:
            return
        
        if self.box:
            self.box.done(0)
        
        self.finished = True
        self.callback(*self.args)
        Message.infoMessage(self, ' ', 'Finished. You can now check log for errors.', QIcon(os.path.join(self.projdir, 'Resources', 'empt.ico')))
        
    def saveLog(self):
        if self.finished:
            dial = QFileDialog()
            dial.setWindowIcon(QIcon(os.path.join(self.projdir, 'Resources', 'save.png'))) #не работает
        
            try:
                name = dial.getSaveFileName(parent=self, caption='Сохранить', filter="Text file (*.txt)")
                full = str(name)[2:len(str(name))-6-17]  #('C:/Users/Nikita/Desktop/image.png', 'Text file (*.txt)')
                
                curdir = os.getcwd()
                with open('temporaryfilelogtodel.txt', 'w') as f:
                    f.write(str(self.edit.toPlainText()))
                    
                shutil.copyfile('temporaryfilelogtodel.txt', full)
                os.remove(os.path.join(curdir, 'temporaryfilelogtodel.txt'))
                
            except Exception:
                dial.accept()
                
    def closeEvent(self, event):
        if self.finished:
            event.accept()
            return
        
        self.box = QMessageBox(self)
        self.box.setText('Building is in progress.\nDo you want to terminate it?')
        self.box.setWindowTitle(' ')
        self.box.setFont(QFont("Calibri", 13))
        self.box.setIcon(QMessageBox.Warning)
        self.box.setWindowIcon(QIcon(os.path.join(self.projdir, "Resources", "empt.ico")))
        
        self.box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        buttons = self.box.findChildren(QPushButton)
        buttons[0].setFont(QFont("Calibri", 11))
        buttons[1].setFont(QFont("Calibri", 11))
        
        ans = self.box.exec_()
        
        
        if ans == QMessageBox.Yes:
            self.qProcess.kill()
            os.chdir(self.projdir)
            shutil.rmtree('tmp2', ignore_errors=True) 
            for button in self.disabled_buttons:
                button.setDisabled(False)
            self.killed = True
            event.accept()
        else:
            event.ignore()
            
        
    