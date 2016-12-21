import os
import sys
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton, QApplication
from PyQt5.QtGui import QIcon, QFont

#Класс для вывода различных QMessageBox с сообщениями
class Message(QWidget):
    
    @staticmethod
    def errorMessage(cur_self, title, text, icon=None):
        rec = QApplication.desktop()
        rec = rec.screenGeometry()
        screenWidth = rec.width()
        box = QMessageBox(cur_self)
        box.setText(text)
        box.setWindowTitle(title)
        if sys.platform == 'linux':
            font = QFont("Liberation Serif")
        else:
            font = QFont("Calibri")
        font.setPixelSize(23 / 1920 * screenWidth)
        box.setFont(font)
        box.setIcon(QMessageBox.Critical)
        if icon is None:
            box.setWindowIcon(QIcon(os.path.join("Resources", "empt.ico")))
        else:
            box.setWindowIcon(QIcon(icon))
        box.setStandardButtons(QMessageBox.Ok)
        
        button = box.findChild(QPushButton)
        font.setPixelSize(22 / 1920 * screenWidth)
        button.setFont(font)
        
        box.exec_()
        
    @staticmethod
    def warningMessage(cur_self, title, text, icon=None):
        rec = QApplication.desktop()
        rec = rec.screenGeometry()
        screenWidth = rec.width()
        box = QMessageBox(cur_self)
        box.setText(text)
        box.setWindowTitle(title)
        if sys.platform == 'linux':
            font = QFont("Liberation Serif")
        else:
            font = QFont("Calibri")
        font.setPixelSize(23 / 1920 * screenWidth)
        box.setFont(font)
        box.setIcon(QMessageBox.Warning)
        if icon is None:
            box.setWindowIcon(QIcon(os.path.join("Resources", "empt.ico")))
        else:
            box.setWindowIcon(QIcon(icon))
        box.setStandardButtons(QMessageBox.Ok)
        
        button = box.findChild(QPushButton)
        font.setPixelSize(22 / 1920 * screenWidth)
        button.setFont(font)
        
        box.exec_()
    
    @staticmethod   
    def infoMessage(cur_self, title, text, icon=None):
        rec = QApplication.desktop()
        rec = rec.screenGeometry()
        screenWidth = rec.width()
        box = QMessageBox(cur_self)
        box.setText(text)
        box.setWindowTitle(title)
        if sys.platform == 'linux':
            font = QFont("Liberation Serif")
        else:
            font = QFont("Calibri")
        font.setPixelSize(23 / 1920 * screenWidth)
        box.setFont(font)
        box.setIcon(QMessageBox.Information)
        if icon is None:
            box.setWindowIcon(QIcon(os.path.join("Resources", "empt.ico")))
        else:
            box.setWindowIcon(QIcon(icon))
        box.setStandardButtons(QMessageBox.Ok)
        
        button = box.findChild(QPushButton)
        font.setPixelSize(22 / 1920 * screenWidth)
        button.setFont(font)
        
        box.exec_()
        
        
        
