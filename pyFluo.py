from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5 import uic
import sys
import serial
import time

UI_MainWindow = uic.loadUiType('MainWindow.ui')[0] # convert .ui to a type object


class mainWindow(QMainWindow, UI_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)	# skeleton part to initiate
        UI_MainWindow .__init__(self)		# the imported UI file
        self.setupUi(self)					#

        #Initialise variables
        self.exp1 = 20
        self.exp2 = 15
        self.exp0 = 20 # wavelength in the 1 wavelength protocol
        self.isi = 100
        self.ifi = 1000
        self.ifi_1w = 1000 # framerate in the 1 wavelength protocol
        self.LED_1w = 0 # which led to use in the 1 w protocol. 0-1 : one of the 2 leds
        self.com = 'COM6'
        self.eventStart = 0
        self.eventStart_1w = 0  # 1 wavelength protocol
        self.eventEnd = 0
        self.eventEnd_1w = 0   #1 wavelength protocol

        self.state2 = 2 # 1: only run the camera, 2: run camera and leds
        # Try to open serial with defaul value
        try:
            self.ser = serial.Serial(self.com,9600, timeout=5, parity=serial.PARITY_EVEN, rtscts=1)
            time.sleep(2)
            self.ser.isOpen()
            self.ser.flushInput()
            self.ser.flushOutput()
            print("serial open")
        except:
            self.ser = None
            self.com = 'None'
            print("serial not open")

    @pyqtSlot()
    def on_comLineEdit_editingFinished(self):
        self.com = str(self.comLineEdit.text())
        print(self.com)
        try:
            self.ser.close()
        except AttributeError:
            pass
        try:
            self.ser = serial.Serial(self.com,9600, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
            time.sleep(2)
            self.ser.isOpen()
            self.ser.flushInput()
            self.ser.flushOutput()
            print("serial open")
        except:
            self.ser = None
            self.com = 'None'
            print("Couldn't open serial")



    @pyqtSlot(int)
    def on_exp1Spin_valueChanged(self, value):
        self.exp1 = value


    @pyqtSlot(int)
    def on_exp2Spin_valueChanged(self, value):
        self.exp2 = value


    @pyqtSlot(int)
    def on_isiSpin_valueChanged(self, value):
        self.isi = value

    @pyqtSlot(int)
    def on_ifiSpin_valueChanged(self, value):
        self.ifi = value

    @pyqtSlot(int)
    def on_eventStartSpinBox_valueChanged(self, value):
        self.eventStart = value

    @pyqtSlot(int)
    def on_eventEndSpinBox_valueChanged(self, value):
        self.eventEnd = value


    @pyqtSlot(bool)
    def on_Led1PushButton_clicked(self):
        message = "3 0 0 0 0 0 0 0"
        self.sendMessage(message)

    @pyqtSlot(bool)
    def on_Led2PushButton_clicked(self):
        message = "4 0 0 0 0 0 0 0"
        self.sendMessage(message)

    @pyqtSlot(bool)
    def on_eventpushButton_clicked(self):
        message = "5 0 0 0 0 0 0 0"
        self.sendMessage(message)

    @pyqtSlot(bool)
    def on_blinkPushButton_clicked(self):
        message = "2 "+str(self.exp1)+" "+str(self.exp2) + " " + str(self.isi) + " " + str(self.ifi) + " " + str(self.eventStart) + " " + str(self.eventEnd) + " " + str(self.state2) + " "
        self.sendMessage(message)

    @pyqtSlot(int)
    def on_interruptCheckBox_stateChanged(self,state):
        if state !=0:
            self.state2 = 2

        else:
            self.state2 = 1

    def sendMessage(self, message):
        #message = "0 0 1 0 0 "+str5+" 0 0 0\n"

        #' the message consists of
        # 1st: 1: turn off, 2: execute protocol, 3: turn led 1 on, 4: turn led 2 on, 5: turn event pin on
        # 2nd: led 1 exposure
        # 3: led 2 exposure
        #4 : delay bertween two leds
        #5 : interframe interval (couple of frames if two wavelengths)
        # 6: event start
        # 7 event end
        # 8th: 1 : camera + leds, 2: camera only, 0: none.

        message = bytearray(message, encoding='utf8')
        print(message)
        #message = b"0 0 1 0 0 30\n"
        self.ser.write(message)

    @pyqtSlot(bool)
    def on_stopButton_clicked(self):
        message =  "1 0 0 0 0 0 0 0"
        self.sendMessage(message)
        ##########################################################
        # Part for 1 led#########################################
    @pyqtSlot(int)
    def on_LEDcomboBox_currentIndexChanged(self,index):
        self.LED_1w = index

    @pyqtSlot(int)
    def on_exp1Spin_2_valueChanged(self, value):
        self.exp0 = value

    @pyqtSlot(int)
    def on_ifiSpin_2_valueChanged(self, value):
        self.ifi_1w = value

    @pyqtSlot(int)
    def on_eventStartSpinBox_2_valueChanged(self, value):
        self.eventStart_1w = value

    @pyqtSlot(int)
    def on_eventEndSpinBox_2_valueChanged(self, value):
        self.eventEnd_1w = value

    @pyqtSlot(bool)
    def on_blinkPushButton_2_clicked(self):
        # Start 1 wavelength protocol
        if self.LED_1w == 0:
            exp0 = self.exp0
            exp1 = 0
        elif self.LED_1w == 1:
            exp1 = self.exp0
            exp0 = 0
        message = "2 "+str(exp0)+" "+str(exp1)+ " " + str(0) + " " + str(self.ifi_1w) + " " + str(self.eventStart_1w)  + " " + str(self.eventEnd_1w) + " " + str(self.state2) + " "
        self.sendMessage(message)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    """
    window.resize(1100,590)
    window.show()

    """
    # """

    # code.interact(local=locals())
    sys.exit(app.exec_())
