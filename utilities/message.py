from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton, QApplication
from PyQt5.QtGui import QIcon, QFont
import os.path
import sys


#Класс для вывода различных QMessageBox с сообщениями
class Message(QWidget):
    
    @staticmethod
    def message(cur_self, title, text, messageType, icon):
        rec = QApplication.desktop()
        rec = rec.screenGeometry()
        screenWidth = rec.width()
        box = QMessageBox(cur_self)
        box.setText(text)
        box.setWindowTitle(title)
        if sys.platform == 'linux':
            font = QFont("Liberation Serif")
        elif sys.platform == 'darwin':
            font = QFont("Times")
        else:
            font = QFont("Calibri")
        font.setPixelSize(23 / 1920 * screenWidth)
        box.setFont(font)
        box.setIcon(messageType)
        if icon is None:
            box.setWindowIcon(QIcon(os.path.join(cur_self.projectDir, "Resources", "empt.ico")))
        else:
            box.setWindowIcon(QIcon(icon))
        box.setStandardButtons(QMessageBox.Ok)
        
        button = box.findChild(QPushButton)
        font.setPixelSize(22 / 1920 * screenWidth)
        button.setFont(font)
        
        box.exec_()
    
    @staticmethod
    def errorMessage(cur_self, title, text, icon=None):
        Message.message(cur_self, title, text, QMessageBox.Critical, icon)
        
    @staticmethod
    def warningMessage(cur_self, title, text, icon=None):
        Message.message(cur_self, title, text, QMessageBox.Warning, icon)
      
    @staticmethod   
    def infoMessage(cur_self, title, text, icon=None):
        Message.message(cur_self, title, text, QMessageBox.Information, icon)
        
        
        
