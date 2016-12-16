import os
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon, QFont

#Класс для вывода различных QMessageBox с сообщениями
class Message(QWidget):
    
    @staticmethod
    def errorMessage(cur_self, title, text):
        box = QMessageBox(cur_self)
        box.setText(text)
        box.setWindowTitle(title)
        box.setFont(QFont("Calibri", 14))
        box.setIcon(QMessageBox.Critical)
        box.setWindowIcon(QIcon(os.path.join("Resources", "empt.ico")))
        box.setStandardButtons(QMessageBox.Ok)
        
        button = box.findChild(QPushButton)
        button.setFont(QFont("Calibri", 11))
        
        box.exec_()
        
    @staticmethod
    def warningMessage(cur_self, title, text):
        box = QMessageBox(cur_self)
        box.setText(text)
        box.setWindowTitle(title)
        box.setFont(QFont("Calibri", 14))
        box.setIcon(QMessageBox.Warning)
        box.setWindowIcon(QIcon(os.path.join("Resources", "empt.ico")))
        box.setStandardButtons(QMessageBox.Ok)
        
        button = box.findChild(QPushButton)
        button.setFont(QFont("Calibri", 11))
        
        box.exec_()
        
        