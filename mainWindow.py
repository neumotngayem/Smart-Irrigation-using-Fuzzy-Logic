# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from resultWindow import Ui_ResultWindow
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("mainUI.ui", self)
        self.btn_calculate.clicked.connect(self.openResultWindow)

    def openResultWindow(self):
        try:
            self.soilMoisture = float(self.input_SoilMoisture.text())
            self.humidity = float(self.input_Humidity.text())
            self.temperature = float(self.input_Temperature.text())
            # Check out of bound
            if(self.soilMoisture < 0 or self.soilMoisture > 60):
                self.showMessageBox('Soil Moisture range from 0 to 60')
                return
            if (self.humidity < 0 or self.humidity > 60):
                self.showMessageBox('Humidity range from 0 to 60')
                return
            if (self.temperature < -10 or self.temperature > 60):
                self.showMessageBox('Temperature range from -10 to 60')
                return
            #Show result window
            self.window = Ui_ResultWindow(self.input_SoilMoisture.text(), self.input_Humidity.text(),
                                          self.input_Temperature.text())
            self.window.show()
        except Exception as exc:
            print(exc)
            #Exception input is not numeric
            self.showMessageBox('Input must be numeric')
    def showMessageBox(self, infoText):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(infoText)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
app = QApplication([])
window = MainWindow()
window.show()
app.exec_()