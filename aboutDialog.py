from PyQt5.QtWidgets import QDialog, QLabel, QApplication, QPushButton
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import os
import sys

#Диалоговое окно содержашее основную информацию о приложении
class About(QDialog):
    def __init__(self):
        super().__init__()
        
        rec = QApplication.desktop()
        rec = rec.screenGeometry()
        self.screenWidth, self.screenHeight = rec.width(), rec.height()
        
        if sys.platform == 'linux':
            font = QFont("Liberation Serif")
        else:
            font = QFont("Calibri")
        
        self.lbl = QLabel("pyBuildManager\nbeta 0.75\n\n©Nikita Morozov 2016", self)
        font.setPixelSize(25 / 1920 * self.screenWidth)
        self.lbl.setFont(font)
        self.lbl.move(10 / 1920 * self.screenWidth, 10 / 1080 * self.screenHeight) 
        
        pal = self.palette()
        role = self.backgroundRole()
        pal.setColor(role, Qt.white)
        
        self.btn = QPushButton("OK", self)
        self.btn.resize(90 / 1920 * self.screenWidth, 30 / 1080 * self.screenHeight)
        self.btn.move(200 / 1920 * self.screenWidth, 150 / 1080 * self.screenHeight)
        font.setPixelSize(21 / 1920 * self.screenWidth)
        self.btn.setFont(font)
        self.btn.clicked.connect(self.done)
        
        self.setFixedSize(300 / 1920 * self.screenWidth, 200 / 1080 * self.screenHeight)
        self.setWindowTitle("About")
        self.setWindowIcon(QIcon(os.path.join("Resources", "question.png")))
        self.setPalette(pal)
        self.setWindowFlags(Qt.Widget)
        self.show()
        
