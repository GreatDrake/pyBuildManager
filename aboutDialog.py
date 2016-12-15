from PyQt5.QtWidgets import QDialog, QLabel, QApplication, QPushButton
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import os

#Диалоговое окно содержашее основную информацию о приложении
class About(QDialog):
    def __init__(self):
        super().__init__()
        
        rec = QApplication.desktop()
        rec = rec.screenGeometry()
        self.screen_width, self.screen_height = rec.width(), rec.height()
        
        self.lbl = QLabel("pyBuildManager\nbeta 0.7\n\n©Nikita Morozov 2016", self)
        self.lbl.setFont(QFont("Calibri", 15 / 1920 * self.screen_width))
        self.lbl.move(10 / 1920 * self.screen_width, 15 / 1080 * self.screen_height) 
        
        pal = self.palette()
        role = self.backgroundRole()
        pal.setColor(role, Qt.white)
        
        self.btn = QPushButton("OK", self)
        self.btn.resize(90, 30)
        self.btn.move(200, 160)
        self.btn.setFont(QFont("Calibri", 11))
        self.btn.clicked.connect(self.done)
        
        self.setFixedSize(300 / 1920 * self.screen_width, 210 / 1920 * self.screen_width)
        self.setWindowTitle("About")
        self.setWindowIcon(QIcon(os.path.join("Resources", "question.png")))
        self.setPalette(pal)
        self.setWindowFlags(Qt.Widget)
        self.show()
        