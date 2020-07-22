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
        self.isi = 100
        self.ifi = 1000
        self.com = 'COM5'
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
    def comLineEdit_editingFinished(self):
        self.com = str(self.comLineEdit.text())
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
        except:
            self.ser = None
            self.com = 'None'

        self.updateValues()

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

    @pyqtSlot(bool)
    def on_Led1PushButton_clicked(self):
        message = "3 0 0 0 0 "
        self.sendMessage(message)

    @pyqtSlot(bool)
    def on_Led2PushButton_clicked(self):
        message = "4 0 0 0 0 "
        self.sendMessage(message)

    @pyqtSlot(bool)
    def on_blinkPushButton_clicked(self):
        message = "2 "+str(self.exp1)+" "+str(self.exp2)+ " " + str(self.isi) + " " + str(self.ifi) + " "
        self.sendMessage(message)

    def sendMessage(self, message):
        #message = "0 0 1 0 0 "+str5+" 0 0 0\n"
        message = bytearray(message, encoding='utf8')
        print(message)
        #message = b"0 0 1 0 0 30\n"
        self.ser.write(message)


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
