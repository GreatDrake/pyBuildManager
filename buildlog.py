import shutil
import os
from message import Message
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QMenuBar, QFileDialog, QAction, QApplication
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QProcess

class BuildLog(QMainWindow):
    def __init__(self, command, callback, projdir, args):    
   
        QMainWindow.__init__(self)
        
        rec = QApplication.desktop()
        rec = rec.screenGeometry()
        self.screenWidth, self.screenHeight = rec.width(), rec.height()
        
        self.finished = False
        
        self.args = args
        self.callback = callback
        self.projdir = projdir
   
        self.edit = QTextEdit(self)
        self.edit.setFont(QFont('Calibri', 12))
        
        self.setCentralWidget(self.edit)
        
        saveAct = QAction(QIcon(os.path.join(self.projdir, 'Resources', 'save.png')),'Save as', self)
        saveAct.triggered.connect(self.saveLog)
        exitAct = QAction(QIcon(os.path.join(self.projdir, 'Resources', 'exit.png')),'Exit', self)
        exitAct.triggered.connect(self.close)
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
        self.finished = True
        self.callback(*self.args)
        Message.infoMessage(self, ' ', 'Finished. You can check log for errors.', QIcon(os.path.join(self.projdir, 'Resources', 'empt.ico')))
        
    def saveLog(self):
        if self.finished:
            dial = QFileDialog()
        
            try:
                name = dial.getSaveFileName(parent=self, caption='Сохранить', filter="Text file (*.txt)")
                full = str(name)[2:len(str(name))-6-17]  #('C:/Users/Nikita/Desktop/image.png', 'Text file (*.txt)')
                
                with open('temporaryfilelogtodel.txt', 'w') as f:
                    f.write(str(self.edit.toPlainText()))
                    
                shutil.copyfile('temporaryfilelogtodel.txt', full)
                os.remove('temporaryfilelogtodel.txt')
            except Exception:
                dial.accept()
        
    