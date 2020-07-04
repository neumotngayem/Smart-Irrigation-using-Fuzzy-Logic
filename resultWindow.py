# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
import math

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random


class Ui_ResultWindow(QMainWindow):

    def __init__(self, soilMoisture, humidity, temperature):
        QMainWindow.__init__(self)
        loadUi("resultUI.ui", self)
        self.btn_exit.clicked.connect(self.closeResultWindow)
        # Input value
        self.input_SoilMoisture = float(soilMoisture)
        self.lbl_SoilMoisture.setText(str(self.input_SoilMoisture)+ ' cB')
        self.input_Humidity = float(humidity)
        self.lbl_Humidity.setText(str(self.input_Humidity)+ ' %')
        self.input_Temperature = float(temperature)
        self.lbl_Temperature.setText(str(self.input_Temperature)+ ' ℃')
        # Init Membership
        self.initSoilMoistureMembership()
        self.initHumidityMembership()
        self.initTemperatureMembership()
        self.initValveOpenMembersip()
        # Calculate Output
        self.calculateOutput()
        self.update_graph()

    # Triangular function
    def tri(self, x, lowerbound, peak, upperbound):
        if (x < lowerbound):
            return (0)
        elif (x > upperbound):
            return (0)
        elif (x <= peak):
            return ((x - lowerbound) / (peak - lowerbound))
        else:
            return ((x - upperbound) / (peak - upperbound))

    # Trapezoidal function
    def trap(self, x, lowerbound, peak1, peak2, upperbound):
        if (x < lowerbound):
            return (0)
        elif (x > upperbound):
            return (0)
        elif (x <= peak1):
            return ((x - lowerbound) / (peak1 - lowerbound))
        elif (x >= peak2):
            return ((x - upperbound) / (peak2 - upperbound))
        else:
            return (1)

    def initSoilMoistureMembership(self):
        self.SoilMoisture = np.linspace(-1, 61, 200)
        self.drySM = np.zeros(len(self.SoilMoisture))
        self.normalSM = np.zeros(len(self.SoilMoisture))
        self.adequateSM = np.zeros(len(self.SoilMoisture))
        self.saturatedSM = np.zeros(len(self.SoilMoisture))
        # Rev 4 -  Inverse the value range
        for i in range(0, len(self.SoilMoisture)):
            # Rev 3 - Change the lowerbound
            self.drySM[i] = self.trap(self.SoilMoisture[i], 30, 36, 59, 61)  # Dry Soil Moisture ranges from 30 to 60 Centibars
            self.normalSM[i] = self.trap(self.SoilMoisture[i], 18, 24, 30,36)  # Normal Soil Moisture ranges from 18 to 36 Centibars
            self.adequateSM[i] = self.trap(self.SoilMoisture[i], 6, 12, 18, 24)  # Adequately Wet Soil Moisture ranges from 6 to 24 Centibars
            # Rev 3 - Change the upperbound
            self.saturatedSM[i] = self.trap(self.SoilMoisture[i], -1, 1, 6, 12)  # Saturated Soil Moisture ranges from 0 to 12 Centibars

    def initHumidityMembership(self):
        # Humidity -> Low / Medium / High / Extremely High
        # Humidity ranges from 0 to 60
        self.Humidity = np.linspace(-1, 61, 200)
        self.lowH = np.zeros(len(self.Humidity))
        self.mediumH = np.zeros(len(self.Humidity))
        self.highH = np.zeros(len(self.Humidity))
        self.extremehighH = np.zeros(len(self.Humidity))

        for i in range(0, len(self.Humidity)):
            # Rev 3 - Change the lowerbound
            self.lowH[i] = self.trap(self.Humidity[i], -1, 1, 10, 20)  # Low Humidity ranges from 0 to 20 percent
            self.mediumH[i] = self.tri(self.Humidity[i], 15, 25, 35)  # Medium Humidity ranges from 15 to 35 percent
            self.highH[i] = self.tri(self.Humidity[i], 30, 40, 50)  # High Humidity ranges from 30 to 50 percent
            # Rev 3 - Change the upperbound
            self.extremehighH[i] = self.trap(self.Humidity[i], 45, 55, 59, 61)  # Extremely High Humidity ranges from 45 to 60 percent

    def initTemperatureMembership(self):
        # Temperature -> Very Cold / Cold / Normal / Hot
        # Temperature ranges from -10 to 60
        self.Temperature = np.linspace(-11, 61, 200)
        self.verycoldT = np.zeros(len(self.Temperature))
        self.coldT = np.zeros(len(self.Temperature))
        self.normalT = np.zeros(len(self.Temperature))
        self.hotT = np.zeros(len(self.Temperature))

        for i in range(0, len(self.Temperature)):
            # Rev 3 - Change the lowerbound
            self.verycoldT[i] = self.trap(self.Temperature[i], -11, -9, 0, 10)  # Very Cold Temperature ranges from -10 to 10 deg C
            self.coldT[i] = self.tri(self.Temperature[i], 5, 15, 25)  # Cold Temperature ranges from 5 to 25 deg C
            self.normalT[i] = self.tri(self.Temperature[i], 20, 30, 40)  # Normal Temperature ranges from 20 to 40 deg C
            # Rev 3 - Change the upperbound
            self.hotT[i] = self.trap(self.Temperature[i], 36, 42, 59, 61)  # Hot Temperature ranges from 36 to 60 deg C

    def initValveOpenMembersip(self):
        self.ValveOpening = np.linspace(-1, 101, 200)
        self.verysmallVO = np.zeros(len(self.ValveOpening))
        self.smallVO = np.zeros(len(self.ValveOpening))
        self.mediumVO = np.zeros(len(self.ValveOpening))
        self.largeVO = np.zeros(len(self.ValveOpening))
        self.fullVO = np.zeros(len(self.ValveOpening))

        for i in range(0, len(self.ValveOpening)):
            # Rev 3 - Change the lowerbound
            self.verysmallVO[i] = self.trap(self.ValveOpening[i], -1, 1, 10, 20)  # Very Small Valve Opening ranges from 0 to 20 percent
            self.smallVO[i] = self.tri(self.ValveOpening[i], 15, 30, 45)  # Small Valve Opening ranges from 15 to 45 percent
            self.mediumVO[i] = self.tri(self.ValveOpening[i], 40, 55, 70)  # Medium Valve Opening ranges from 40 to 70 percent
            self.largeVO[i] = self.tri(self.ValveOpening[i], 65, 75, 85)  # Large Valve Opening ranges from 65 to 85 percent
            # Rev 3 - Change the upperbound
            self.fullVO[i] = self.trap(self.ValveOpening[i], 80, 90, 99, 101)  # Full Valve Opening ranges from 80 to 100 percent

    def calculateOutput(self):
        # Rev 4 -  Inverse the value range
        # Rev 3 - Change the lowerbound
        self.dry_SoilMoisture_mbr = self.trap(self.input_SoilMoisture, 30, 36, 59, 61)  # Dry Soil Moisture ranges from 30 to 60 Centibars
        self.normal_SoilMoisture_mbr = self.trap(self.input_SoilMoisture, 18, 24, 30,36)  # Normal Soil Moisture ranges from 18 to 36 Centibars
        self.adequate_SoilMoisture_mbr = self.trap(self.input_SoilMoisture, 6, 12, 18, 24)  # Adequately Wet Soil Moisture ranges from 6 to 24
        # Rev 3 - Change the upperbound
        self.saturated_SoilMoisture_mbr = self.trap(self.input_SoilMoisture, -1, 1, 6, 12)  # Saturated Soil Moisture ranges from 0 to 12 Centibars
        # Rev 3 - Change the lowerbound
        self.low_Humidity_mbr = self.trap(self.input_Humidity, -1, 1, 10, 20)  # Low Humidity ranges from 0 to 20 percent
        self.medium_Humidity_mbr = self.tri(self.input_Humidity, 15, 25, 35)  # Medium Humidity ranges from 15 to 35 percent
        self.high_Humidity_mbr = self.tri(self.input_Humidity, 30, 40, 50)  # High Humidity ranges from 30 to 50 percent
        # Rev 3 - Change the upperbound
        self.extremehigh_Humidity_mbr = self.trap(self.input_Humidity, 45, 55, 59,
                                        61)  # Extremely High Humidity ranges from 45 to 60 percent
        # Rev 3 - Change the lowerbound
        self.verycold_Temperature_mbr = self.trap(self.input_Temperature, -11, -9, 0,
                                        10)  # Very Cold Temperature ranges from -10 to 10 deg C
        self.cold_Temperature_mbr = self.tri(self.input_Temperature, 5, 15, 25)  # Cold Temperature ranges from 5 to 25 deg C
        self.normal_Temperature_mbr = self.tri(self.input_Temperature, 20, 30, 40)  # Normal Temperature ranges from 20 to 40 deg C
        # Rev 3 - Change the upperbound
        self.hot_Temperature_mbr = self.trap(self.input_Temperature, 36, 42, 59, 61)  # Hot Temperature ranges from 36 to 60 deg C

        ## Evaluation of rule-1 : Dry Soil Moisture and Low Humidity and Hot Temperature x Full Valve Opening
        self.A1 = np.zeros(len(self.fullVO))
        self.r1 = min(self.dry_SoilMoisture_mbr, self.low_Humidity_mbr, self.hot_Temperature_mbr)

        for i in range(0, len(self.fullVO)):
            self.A1[i] = min(self.r1, self.fullVO[i])

        ## Evaluation of rule-2, rule-3, rule-5 and rule-7:
        # (Dry Soil Moisture and Low Humidity and Normal Temperature) OR
        # (Dry Soil Moisture and Low Humidity and Cold Temperature) OR
        # (Normal Soil Moisture and Medium Humidity and Very Cold Temperature) OR
        # (Normal Soil Moisture and Extremely High Humidity and Normal Temperature)
        # x Large Valve Opening
        self.A2 = np.zeros(len(self.largeVO))
        # Evaluate each rule with AND condition
        self.r2 = min(self.dry_SoilMoisture_mbr, self.low_Humidity_mbr, self.normal_Temperature_mbr)
        self.r3 = min(self.dry_SoilMoisture_mbr, self.low_Humidity_mbr, self.cold_Temperature_mbr)
        self.r5 = min(self.normal_SoilMoisture_mbr, self.medium_Humidity_mbr, self.verycold_Temperature_mbr)
        self.r7 = min(self.normal_SoilMoisture_mbr, self.extremehigh_Humidity_mbr, self.normal_Temperature_mbr)

        # Evaluate the rules with OR condition
        # @Bac change here a bit for made the program more clearly
        self.rct_LargeVO = max(self.r2, self.r3, self.r5, self.r7)

        # Multiply with output membership
        for i in range(0, len(self.largeVO)):
            self.A2[i] = min(self.rct_LargeVO, self.largeVO[i])

        # @Bac continue from here...
        ## Evaluation of rule-4 and rule-6:
        # (Dry Soil Moisture and Low Humidity and Very Cold Temperature) OR
        # (Normal Soil Moisture and High Humidity and Cold Temperature)
        # x Medium Valve Opening
        self.A3 = np.zeros(len(self.mediumVO))
        # Evaluate each rule with AND condition
        self.r4 = min(self.dry_SoilMoisture_mbr, self.low_Humidity_mbr, self.verycold_Temperature_mbr)
        self.r6 = min(self.normal_SoilMoisture_mbr, self.high_Humidity_mbr, self.cold_Temperature_mbr)
        # Evaluate the rules with OR condition
        self.rct_MediumVO = max(self.r4, self.r6)
        # Multiply with output membership
        for i in range(0, len(self.mediumVO)):
            self.A3[i] = min(self.rct_MediumVO, self.mediumVO[i])

        ## Evaluation of rule-8, rule-9, rule-10, rule-11, rule-12 and rule-17:
        # (Adequately Wet Soil Moisture and Low Humidity and Normal Temperature) OR
        # (Adequately Wet Soil Moisture and Medium Humidity and Normal Temperature) OR
        # (Adequately Wet Soil Moisture and High Humidity and Normal Temperature) OR
        # (Saturated Soil Moisture and Low Humidity and Normal Temperature) OR
        # (Saturated Soil Moisture and Medium Humidity and Normal Temperature) OR
        # (Saturated Soil Moisture and Extremely High Humidity and Normal Temperature)
        # x Small Valve Opening
        self.A4 = np.zeros(len(self.smallVO))
        # Evaluate each rule with AND condition
        self.r8 = min(self.adequate_SoilMoisture_mbr, self.low_Humidity_mbr, self.normal_Temperature_mbr)
        self.r9 = min(self.adequate_SoilMoisture_mbr, self.medium_Humidity_mbr, self.normal_Temperature_mbr)
        self.r10 = min(self.adequate_SoilMoisture_mbr, self.high_Humidity_mbr, self.normal_Temperature_mbr)
        self.r11 = min(self.saturated_SoilMoisture_mbr, self.low_Humidity_mbr, self.normal_Temperature_mbr)
        self.r12 = min(self.saturated_SoilMoisture_mbr, self.medium_Humidity_mbr, self.normal_Temperature_mbr)
        self.r17 = min(self.saturated_SoilMoisture_mbr, self.extremehigh_Humidity_mbr, self.normal_Temperature_mbr)
        # Evaluate the rules with OR condition
        self.rct_SmallVO = max(self.r8, self.r9, self.r10, self.r11, self.r12, self.r17)
        # Multiply with output membership
        for i in range(0, len(self.smallVO)):
            self.A4[i] = min(self.rct_SmallVO, self.smallVO[i])

        ## Evaluation of rule-13, rule-14, rule-15 and rule-16:
        # (Saturated Soil Moisture and Low Humidity and Very Cold Temperature) OR
        # (Saturated Soil Moisture and Extremely High Humidity and Very Cold Temperature) OR
        # (Adequately Wet Soil Moisture and High Humidity and Very Cold Temperature) OR
        # (Saturated Soil Moisture and Extremely High Humidity and Very Cold Temperature) OR
        # x Very Small Valve Opening
        self.A5 = np.zeros(len(self.verysmallVO))
        # Evaluate each rule with AND condition
        self.r13 = min(self.saturated_SoilMoisture_mbr, self.low_Humidity_mbr, self.verycold_Temperature_mbr)
        self.r14 = min(self.saturated_SoilMoisture_mbr, self.extremehigh_Humidity_mbr, self.verycold_Temperature_mbr)
        self.r15 = min(self.adequate_SoilMoisture_mbr, self.high_Humidity_mbr, self.verycold_Temperature_mbr)
        self.r16 = min(self.saturated_SoilMoisture_mbr, self.extremehigh_Humidity_mbr, self.verycold_Temperature_mbr)
        # Evaluate the rules with OR condition
        self.rct_VerySmallVO = max(self.r13, self.r14, self.r15, self.r16)
        # Multiply with output membership
        for i in range(0, len(self.verysmallVO)):
            self.A5[i] = min(self.rct_VerySmallVO, self.verysmallVO[i])

        ## Consolidation of rules
        self.A = np.zeros(len(self.A1))
        for i in range(0, len(self.A1)):
            self.A[i] = max(self.A1[i], self.A2[i], self.A3[i], self.A4[i], self.A5[i])
        ## Centroid calculation
        with np.errstate(invalid='raise'):
            try:
                self.centroid = np.trapz(self.A * self.ValveOpening, self.ValveOpening) / (np.trapz(self.A, self.ValveOpening))
                self.centroid = round(self.centroid, 3)
                print('Valve Opening = ', self.centroid)
                self.lbl_ValveOpen.setText(str(self.centroid) + ' %')
            except FloatingPointError:
                print('Valve Opening = ', 0)
                self.lbl_ValveOpen.setText(str(0) + ' %')
    def update_graph(self):
        #Soil Moisture Membership Plot
        self.MplSoilMoisture.canvas.axes.clear()
        self.MplSoilMoisture.canvas.axes.plot(self.SoilMoisture, self.drySM, color='red', label='Dry')
        self.MplSoilMoisture.canvas.axes.plot(self.SoilMoisture, self.normalSM, color='green', label='Normal')
        self.MplSoilMoisture.canvas.axes.plot(self.SoilMoisture, self.adequateSM, color='blue', label='Adequately Wet')
        self.MplSoilMoisture.canvas.axes.plot(self.SoilMoisture, self.saturatedSM, color='black', label='Saturated')
        self.MplSoilMoisture.canvas.axes.set_title("Soil Moisture")
        self.MplSoilMoisture.canvas.axes.set_xlabel('Centibars')
        self.MplSoilMoisture.canvas.axes.set_ylabel('Membership')
        self.MplSoilMoisture.canvas.axes.legend()
        self.MplSoilMoisture.canvas.draw()
        # Humidity Membership Plot
        self.MplHumidity.canvas.axes.clear()
        self.MplHumidity.canvas.axes.plot(self.Humidity, self.lowH, color='red', label='Low')
        self.MplHumidity.canvas.axes.plot(self.Humidity, self.mediumH, color='green', label='Medium')
        self.MplHumidity.canvas.axes.plot(self.Humidity, self.highH, color='blue', label='High')
        self.MplHumidity.canvas.axes.plot(self.Humidity, self.extremehighH, color='black', label='Extremely High')
        self.MplHumidity.canvas.axes.set_title("Humidity")
        self.MplHumidity.canvas.axes.set_xlabel('Percent')
        self.MplHumidity.canvas.axes.set_ylabel('Membership')
        self.MplHumidity.canvas.axes.legend()
        self.MplHumidity.canvas.draw()
        # Temperature Membership Plot
        self.MplTemperature.canvas.axes.clear()
        self.MplTemperature.canvas.axes.set_title("Temperature")
        self.MplTemperature.canvas.axes.set_xlabel('Deg C')
        self.MplTemperature.canvas.axes.set_ylabel('Membership')
        self.MplTemperature.canvas.axes.plot(self.Temperature, self.verycoldT, color='red', label='Very Cold')
        self.MplTemperature.canvas.axes.plot(self.Temperature, self.coldT, color='green', label='Cold')
        self.MplTemperature.canvas.axes.plot(self.Temperature, self.normalT, color='blue', label='Normal')
        self.MplTemperature.canvas.axes.plot(self.Temperature, self.hotT, color='black', label='Hot')
        self.MplTemperature.canvas.axes.legend()
        self.MplTemperature.canvas.draw()
        # Valve Open Membership Plot
        self.MplValveOpen.canvas.axes.clear()
        self.MplValveOpen.canvas.axes.set_title("Valve Opening")
        self.MplValveOpen.canvas.axes.set_xlabel('Percent')
        self.MplValveOpen.canvas.axes.set_ylabel('Membership')
        self.MplValveOpen.canvas.axes.plot(self.ValveOpening, self.verysmallVO, color='red', label='Very Small')
        self.MplValveOpen.canvas.axes.plot(self.ValveOpening, self.smallVO, color='green', label='Small')
        self.MplValveOpen.canvas.axes.plot(self.ValveOpening, self.mediumVO, color='blue', label='Medium')
        self.MplValveOpen.canvas.axes.plot(self.ValveOpening, self.largeVO, color='brown', label='Large')
        self.MplValveOpen.canvas.axes.plot(self.ValveOpening, self.fullVO, color='black', label='Full')
        # Result drawing
        self.MplValveOpen.canvas.axes.plot(self.ValveOpening, self.A, linestyle='dashed', color='yellow')
        self.MplValveOpen.canvas.axes.fill_between(self.ValveOpening, self.A, color='grey')
        self.MplValveOpen.canvas.axes.legend()
        self.MplValveOpen.canvas.draw()
    def closeResultWindow(self):
        self.hide()


