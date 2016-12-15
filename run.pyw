#Запуск приложения
from mainWindow import Window
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
w = Window()
sys.exit(app.exec_())
