#Запуск приложения
from PyQt5.QtWidgets import QApplication
from mainWindow import Window
import sys

app = QApplication(sys.argv)
w = Window()
sys.exit(app.exec_())
