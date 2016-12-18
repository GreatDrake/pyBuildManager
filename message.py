import os
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon, QFont

#Класс для вывода различных QMessageBox с сообщениями
class Message(QWidget):
    
    @staticmethod
    def errorMessage(cur_self, title, text, icon=None):
        box = QMessageBox(cur_self)
        box.setText(text)
        box.setWindowTitle(title)
        box.setFont(QFont("Calibri", 13))
        box.setIcon(QMessageBox.Critical)
        if icon is None:
            box.setWindowIcon(QIcon(os.path.join("Resources", "empt.ico")))
        else:
            box.setWindowIcon(QIcon(icon))
        box.setStandardButtons(QMessageBox.Ok)
        
        button = box.findChild(QPushButton)
        button.setFont(QFont("Calibri", 11))
        
        box.exec_()
        
    @staticmethod
    def warningMessage(cur_self, title, text, icon=None):
        box = QMessageBox(cur_self)
        box.setText(text)
        box.setWindowTitle(title)
        box.setFont(QFont("Calibri", 13))
        box.setIcon(QMessageBox.Warning)
        if icon is None:
            box.setWindowIcon(QIcon(os.path.join("Resources", "empt.ico")))
        else:
            box.setWindowIcon(QIcon(icon))
        box.setStandardButtons(QMessageBox.Ok)
        
        button = box.findChild(QPushButton)
        button.setFont(QFont("Calibri", 11))
        
        box.exec_()
    
    @staticmethod   
    def infoMessage(cur_self, title, text, icon=None):
        box = QMessageBox(cur_self)
        box.setText(text)
        box.setWindowTitle(title)
        box.setFont(QFont("Calibri", 13))
        box.setIcon(QMessageBox.Information)
        if icon is None:
            box.setWindowIcon(QIcon(os.path.join("Resources", "empt.ico")))
        else:
            box.setWindowIcon(QIcon(icon))
        box.setStandardButtons(QMessageBox.Ok)
        
        button = box.findChild(QPushButton)
        button.setFont(QFont("Calibri", 11))
        
        box.exec_()
        
        
        
