from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import os,sys,time,socket,struct,keyboard
import message_navigation_pb2
speed_data = message_navigation_pb2.Message_NavSpeed()

F4kCommandPort = 15003
F4kAddr = ('192.168.192.4', F4kCommandPort)

class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(310, 211)
        self.temp_x = 0.0
        self.temp_rotate = 0.0
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 72, 15))
        self.label.setObjectName("label")
        self.pb_a = QtWidgets.QPushButton(self.centralwidget)
        self.pb_a.setGeometry(QtCore.QRect(35, 111, 73, 69))
        self.pb_a.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./icon/A.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_a.setIcon(icon)
        self.pb_a.setIconSize(QtCore.QSize(60, 60))
        self.pb_a.setObjectName("pb_a")
        self.ln_x = QtWidgets.QLCDNumber(self.centralwidget)
        self.ln_x.setGeometry(QtCore.QRect(30, 20, 64, 23))
        self.ln_x.setObjectName("ln_x")
        self.pb_w = QtWidgets.QPushButton(self.centralwidget)
        self.pb_w.setGeometry(QtCore.QRect(128, 13, 73, 69))
        self.pb_w.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./icon/W.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_w.setIcon(icon1)
        self.pb_w.setIconSize(QtCore.QSize(60, 60))
        self.pb_w.setObjectName("pb_w")
        self.pb_d = QtWidgets.QPushButton(self.centralwidget)
        self.pb_d.setGeometry(QtCore.QRect(222, 111, 73, 69))
        self.pb_d.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./icon/D.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_d.setIcon(icon2)
        self.pb_d.setIconSize(QtCore.QSize(60, 60))
        self.pb_d.setObjectName("pb_d")
        self.pb_s = QtWidgets.QPushButton(self.centralwidget)
        self.pb_s.setGeometry(QtCore.QRect(130, 110, 73, 69))
        self.pb_s.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("./icon/S.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_s.setIcon(icon3)
        self.pb_s.setIconSize(QtCore.QSize(60, 60))
        self.pb_s.setObjectName("pb_s")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 72, 15))
        self.label_2.setObjectName("label_2")
        self.ln_w = QtWidgets.QLCDNumber(self.centralwidget)
        self.ln_w.setGeometry(QtCore.QRect(30, 60, 64, 23))
        self.ln_w.setObjectName("ln_w")
        self.pushButton = QtWidgets.QPushButton("EDU", self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(210, 20, 91, 19))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton("RESET", self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(210, 50, 91, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.eduMode)
        self.pushButton_3.clicked.connect(self.reset407)
        self.thread1 = sendSpeedThread()
        self.thread1.start()

        self.thread2 = listenWThread()
        self.thread2.signal.connect(self.pbW)
        self.thread2.signal.connect(self.pbS)
        self.thread2.signal.connect(self.pbA)
        self.thread2.signal.connect(self.pbD)
        self.thread2.start()
    
    def reset407(self):
        arg = [0xffffffff]
        msg = struct.pack('<' + str(len(arg) + 1) + 'I', 0x0000101E, *arg)
        so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        so.settimeout(0.05)
        so.sendto(msg, F4kAddr)
        so.close()

    def eduMode(self):
        arg = [0xffffffff]
        msg = struct.pack('<' + str(len(arg) + 1) + 'I', 0x00001075, *arg)
        so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        so.settimeout(0.05)
        so.sendto(msg, F4kAddr)
        so.close()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "speed-control"))
        self.label.setText(_translate("MainWindow", "x"))
        self.label_2.setText(_translate("MainWindow", "w"))
    
    def pbW(self):
        if self.pb_w.isDown() or keyboard.is_pressed('w'): 
            self.temp_x = self.temp_x + 0.05
            if self.temp_x >= 0.5:
                self.temp_x = 0.5
            speed_data.x = self.temp_x
            print("temp_x is " + str(self.temp_x))
        elif (not self.pb_s.isDown()) and (not keyboard.is_pressed('s')):
            self.temp_x = 0.0
            speed_data.x = self.temp_x
    
    def pbS(self):
        if self.pb_s.isDown() or keyboard.is_pressed('s'): 
            self.temp_x = self.temp_x - 0.05
            if self.temp_x <= -0.5:
                self.temp_x = -0.5
            speed_data.x = self.temp_x
            print("temp_x is " + str(self.temp_x))
        elif (not self.pb_w.isDown()) and (not keyboard.is_pressed('w')):
            self.temp_x = 0.0
            speed_data.x = self.temp_x

    def pbA(self):
        if self.pb_a.isDown() or keyboard.is_pressed('a'): 
            self.temp_rotate = self.temp_rotate + 0.05
            if self.temp_rotate >= 0.5:
                self.temp_rotate = 0.5
            speed_data.rotate = self.temp_rotate
            print("temp_rotate is " + str(self.temp_rotate))
        elif (not self.pb_d.isDown()) and (not keyboard.is_pressed('d')):
            self.temp_rotate = 0.0
            speed_data.rotate = self.temp_rotate

    def pbD(self):
        if self.pb_d.isDown()  or keyboard.is_pressed('d'): 
            self.temp_rotate = self.temp_rotate - 0.05
            if self.temp_rotate <= -0.5:
                self.temp_rotate = -0.5
            speed_data.rotate = self.temp_rotate
            print("temp_rotate is " + str(self.temp_rotate))
        elif (not self.pb_a.isDown()) and (not keyboard.is_pressed('a')):
            self.temp_rotate = 0.0
            speed_data.rotate = self.temp_rotate

class sendSpeedThread(QThread):
    signal = pyqtSignal()    
    def run(self):
    	while(1):   
            so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            so.settimeout(0.5)
            while(1):
                speed_data_string = speed_data.SerializeToString()
                self.signal.emit()
                time.sleep(0.1)
                so.sendto(struct.pack('<I' + str(len(speed_data_string)) + 's', 0x00001034, speed_data_string), F4kAddr)
            so.close()

class listenWThread(QThread):
    signal = pyqtSignal() 
    def run(self):
    	while(1):
            self.signal.emit()
            time.sleep(0.1)
            
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

