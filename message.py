import os
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtGui import QIcon

#Класс для вывода различных QMessageBox с сообщениями
class Message(QWidget):
    
    @staticmethod
    def errorMessage(cur_self, title, text):
        box = QMessageBox(cur_self)
        box.setText(text)
        box.setWindowTitle(title)
        box.setIcon(QMessageBox.Critical)
        box.setWindowIcon(QIcon(os.path.join("Resources", "empt.ico")))
        box.setStandardButtons(QMessageBox.Ok)
        box.exec_()