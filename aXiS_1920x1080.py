#from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.Qt import *

#additional
#from PyQt5.QtWidgets import *
#from PyQt5.QtCore import *

import sys, time
from time import strftime
from datetime import datetime
from PyQt5.uic import loadUi
import csv

################################################
#SCREEN ADJUSTMENT CALCULATIONS FOR HOMESCREEN

#Label_W= 141
#Label_W= 150
Label_W= 200
Label_H= 40
Line_W= 300
Line_H= 40

NewUser_W= 110
NewUser_H= 40

#label_time_W= 205
#label_time_W= 245
label_time_W= 350
label_time_H= 60 #see fontsize
#label_date_W= 180
label_date_W= 220
label_date_H= 18 #see fontsize

widget_gap_W = 20
widget_gap_H = 20

screen_W_allowance = 20
screen_H_allowance = 40

Whole_Line_H= Label_W+Line_W+widget_gap_W

adj_W = 0


class AddUser(QDialog):
    def __init__(self, *args, **kwargs):
        super(AddUser, self).__init__(*args, **kwargs)
        loadUi("newUser.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        

import sys
class Maintenance(QMainWindow):
    def __init__(self):
        super().__init__()
        self.launchUi()

        self._want_to_close = False #disable the X button for exit

    #disable the X button for exit
    def closeEvent(self, evnt):
        if self._want_to_close:
            QtGui.QWidget.closeEvent(evnt)
        else:
            evnt.ignore()
            #self.setWindowState(QtCore.Qt.WindowMinimized)
        
    def closeApp(self, event):
        self.checkBox.setChecked(False)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.lineEdit_2.clear()
        
        msgBox = QMessageBox(QMessageBox.Question,"aXiS","Are you sure you want to quit aXiS application?",QMessageBox.Yes | QMessageBox.No,parent=None, )
        msgBox.setWindowIcon(QtGui.QIcon('ui\\xray_150x150.png'))
        msgBox.setStyleSheet("QLabel{ color: rgb(0, 0, 0)}")
        msgBox.setFont(QFont('Bahnschrift', 14))
        reply=msgBox.exec_()
        msgBox.deleteLater()

        if reply == QMessageBox.Yes:
            self.get_timeOut()
            #print('Yes')
            mode = 'Maintenance - Shutdown AXIS Application'
            #print (mode)

            with open('data\\log\\XRay_Monitoring.csv', 'r') as f:
                reader = csv.DictReader(f, delimiter=',')
                # All rows
                rows = list(reader)
                # Update last row
                rows[-1].update({'TimeOut': timeOut, 'Mode': mode, 'Voltage': '', 'Current': ''})

            with open('data\\log\\XRay_Monitoring.csv', 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames = rows[-1].keys())
                writer.writeheader()
                writer.writerows(rows)

            with open('data\\log\\superlog.txt', 'a') as f:    
                print (mode, file=f)
                print('Time-out', timeOut, '\n', file=f)
            #print('Yes') 
            sys.exit()
            
            
        else:
            pass

    def launchUi(self):
        loadUi('ui\\maintenance_gui01.ui', self)
        self.setWindowTitle("aXiS (c) jcsaludares")
        self.setWindowIcon(QtGui.QIcon('ui\\xray_150x150.png'))
        #self.resize(734, 535)
        self.setFixedSize(734, 535)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        
        self.pushButton_3.clicked.connect(self.showMinimized)   #minimize

        self.checkBox.stateChanged.connect(self.deSelect)       #HPT
        self.checkBox_2.stateChanged.connect(self.deSelect)     #Start-all
        self.checkBox_3.stateChanged.connect(self.deSelect)     #Others
        

        self.lineEdit_2.setStyleSheet("color:  rgb(219, 156, 10)")     

        self.pushButton_2.clicked.connect(self.check_Entry)
        self.pushButton_4.clicked.connect(self.closeApp)
        

    def deSelect(self,state):
        if state == Qt.Checked:

            if self.sender()==self.checkBox:
                self.checkBox_2.setChecked(False)
                self.checkBox_3.setChecked(False)
                self.lineEdit_2.setEnabled(False)
                self.lineEdit_2.clear()               

            if self.sender()==self.checkBox_2:
                self.checkBox.setChecked(False)
                self.checkBox_3.setChecked(False)
                self.lineEdit_2.setEnabled(False)
                self.lineEdit_2.clear()            

            elif self.sender()==self.checkBox_3:
                self.checkBox_2.setChecked(False)
                self.checkBox.setChecked(False)
                
                #self.lineEdit.clear()
                #self.lineEdit_2.clear()
                #self.lineEdit.setEnabled(False)
                self.lineEdit_2.setEnabled(True)

    def check_Entry(self):
        
        if (self.checkBox.isChecked() ==False and self.checkBox_2.isChecked() ==False and self.checkBox_3.isChecked() ==False):
            #print('error in checkbox')
            msgBox = QMessageBox(QMessageBox.Warning,"aXiS","Please select a checkbox",parent=self,)
            msgBox.setWindowIcon(QtGui.QIcon('ui\\xray_150x150.png'))
            msgBox.setStyleSheet("QLabel{ color: rgb(219, 156, 10)}")
            msgBox.setFont(QFont('Bahnschrift', 15))
            msgBox.exec_()
           

        elif (self.checkBox_3.isChecked() ==True and self.lineEdit_2.text()== ""):
            #print ('missing value')
            #print ('ok')
            msgBox = QMessageBox(QMessageBox.Warning,"aXiS","Please enter operation performed",parent=self,)
            msgBox.setWindowIcon(QtGui.QIcon('ui\\xray_150x150.png'))
            msgBox.setStyleSheet("QLabel{ color: rgb(219, 156, 10)}")
            msgBox.setFont(QFont('Bahnschrift', 15))
            msgBox.exec_()
           
        else:
            #print ('ok n')            
            self.logData()
            self.ret_Home()

    def logData(self):
        self.get_timeOut()

        if self.checkBox_3.isChecked()== True:

            remarks = self.lineEdit_2.text()
            mode = 'Maintenance - Others' + ' (' + remarks + ')'
            #print(mode)

        elif self.checkBox.isChecked()== True:
            mode = 'Maintenance - HPT'
            #print(mode)

        elif self.checkBox_2.isChecked()== True:
            mode = 'Maintenance - Start-all'
            #print(mode)

        with open('data\\log\\XRay_Monitoring.csv', 'r') as f:
            reader = csv.DictReader(f, delimiter=',')
            # All rows
            rows = list(reader)
            # Update last row
            rows[-1].update({'TimeOut': timeOut, 'Mode': mode, 'Voltage': '', 'Current': ''})

        with open('data\\log\\XRay_Monitoring.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames = rows[-1].keys())
            writer.writeheader()
            writer.writerows(rows)
            
        with open('data\\log\\superlog.txt', 'a') as f:    
            print (mode, file=f)
            print('Time-out', timeOut, '\n', file=f)

    def get_timeOut(self):
        global timeOut
        now=datetime.now()
        timeOut=now.strftime("%m/%d/%Y %H:%M:%S")
        
    def ret_Home(self):        
        self.lineEdit_2.clear()       
        self.w = MainWindow()
        self.w.showFullScreen()
        self.kill()

    def kill(self):
        self.destroy()

#class LogOut(QtWidgets.QWidget):
#    def __init__(self, *args, **kwargs):
#        super(LogOut, self).__init__(*args, **kwargs)
        #super().__init__(*args, **kwargs)


class LogOut(QMainWindow):
    def __init__(self):
        super().__init__()
        self.launchUi()
        self._want_to_close = False

    def closeEvent(self, evnt):
        if self._want_to_close:
            QtGui.QWidget.closeEvent(evnt)
        else:
            evnt.ignore()
            #self.setWindowState(QtCore.Qt.WindowMinimized)

    def launchUi(self):
        loadUi('ui\\xray_gui.ui', self)
        self.setWindowTitle("aXiS (c) jcsaludares")
        self.setWindowIcon(QtGui.QIcon('ui\\xray_150x150.png'))

        #self.resize(734, 535)
        self.setFixedSize(734, 535)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        #self.showMinimized()  
        
        #self.pushButton_4.setAutoDefault(True)        
        self.pushButton_3.clicked.connect(self.showMinimized)
        self.checkBox.stateChanged.connect(self.deSelect)
        self.checkBox_2.stateChanged.connect(self.deSelect)
        self.checkBox_3.stateChanged.connect(self.deSelect)        

        self.lineEdit.setStyleSheet("color:  rgb(219, 156, 10)")
        self.lineEdit_2.setStyleSheet("color:  rgb(219, 156, 10)")
        self.lineEdit_3.setStyleSheet("color:  rgb(219, 156, 10)")

        self.onlyInt = QIntValidator()
        self.lineEdit.setValidator(self.onlyInt)
        self.lineEdit_2.setValidator(self.onlyInt)
        self.lineEdit_3.setValidator(self.onlyInt)
        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_3.setEnabled(False)
       
        self.pushButton_4.clicked.connect(self.maintenance)
        self.pushButton_2.clicked.connect(self.check_Entry)

    def maintenance(self):
        #print('pushB 4')
        #global owners_repo
   
        if rfidTag not in owners_repo:      
            msgBox = QMessageBox(QMessageBox.Warning,"aXiS","Operation not allowed for this user!",parent=self,)
            msgBox.setWindowIcon(QtGui.QIcon('ui\\xray_150x150.png'))
            msgBox.setStyleSheet("QLabel{ color: rgb(219, 156, 10)}")
            msgBox.setFont(QFont('Bahnschrift', 15))
            msgBox.exec_()
        
        else:
            #print('ok')
            self.show_maintenance()

    def show_maintenance(self):
        #self.showNormal()
        #self.hide()        
        self.f = Maintenance()
        self.f.show()
        self.kill()


    def deSelect(self,state):
        if state == Qt.Checked:

            if self.sender()==self.checkBox:
                #self.checkBox_2.setChecked(False)
                self.checkBox_3.setChecked(False)
                self.lineEdit.setEnabled(True)
                self.lineEdit_2.setEnabled(True)
                self.lineEdit_3.setEnabled(True)

            if self.sender()==self.checkBox_2:
                #self.checkBox.setChecked(False)
                self.checkBox_3.setChecked(False)
                self.lineEdit.setEnabled(True)
                self.lineEdit_2.setEnabled(True)
                self.lineEdit_3.setEnabled(True)

            elif self.sender()==self.checkBox_3:
                self.checkBox_2.setChecked(False)
                self.checkBox.setChecked(False)
                
                self.lineEdit.clear()
                self.lineEdit_2.clear()
                self.lineEdit_3.clear()
                self.lineEdit.setEnabled(False)
                self.lineEdit_2.setEnabled(False)
                self.lineEdit_3.setEnabled(False)
            
            
    def check_Entry(self):
        if (self.checkBox.isChecked() ==False and self.checkBox_2.isChecked() ==False and self.checkBox_3.isChecked() ==False):
            #print('error in checkbox')
            msgBox = QMessageBox(QMessageBox.Warning,"aXiS","Please select a checkbox",parent=self,)
            msgBox.setWindowIcon(QtGui.QIcon('ui\\xray_150x150.png'))
            msgBox.setStyleSheet("QLabel{ color: rgb(219, 156, 10)}")
            msgBox.setFont(QFont('Bahnschrift', 15))
            msgBox.exec_()
            

        elif (self.checkBox.isChecked() ==True or self.checkBox_2.isChecked()) ==True and (self.lineEdit.text()== "" or self.lineEdit_2.text()== ""):
            #print ('missing value')
            msgBox = QMessageBox(QMessageBox.Warning,"aXiS","Please enter tube settings used",parent=self,)
            msgBox.setWindowIcon(QtGui.QIcon('ui\\xray_150x150.png'))
            msgBox.setStyleSheet("QLabel{ color: rgb(219, 156, 10)}")
            msgBox.setFont(QFont('Bahnschrift', 15))
            msgBox.exec_()

        elif (self.checkBox.isChecked() ==True or self.checkBox_2.isChecked()) ==True and (self.lineEdit_3.text()== ""):
            #print ('missing value')
            msgBox = QMessageBox(QMessageBox.Warning,"aXiS","Please enter number of units inspected",parent=self,)
            msgBox.setWindowIcon(QtGui.QIcon('ui\\xray_150x150.png'))
            msgBox.setStyleSheet("QLabel{ color: rgb(219, 156, 10)}")
            msgBox.setFont(QFont('Bahnschrift', 15))
            msgBox.exec_()

           
        else:
            #print ('ok')            
            self.logData()
            self.ret_Home()

    def logData(self):
        self.get_timeOut()
        
        if self.checkBox_3.isChecked()== True:
            mode = 'Other'
            kV = ''
            uA = ''
            qty= ''
            #print(mode)
            
        elif (self.checkBox.isChecked()== True and self.checkBox_2.isChecked()== True):
            mode = '2D and 3D X-ray'
            kV = self.lineEdit.text()
            uA = self.lineEdit_2.text()
            qty = self.lineEdit_3.text()
            #print(mode)

        elif self.checkBox.isChecked()== True:
            mode = '2D X-ray'
            kV = self.lineEdit.text()
            uA = self.lineEdit_2.text()
            qty = self.lineEdit_3.text()
            #print(mode)

        elif self.checkBox_2.isChecked()== True:
            mode = '3D X-ray'
            kV = self.lineEdit.text()
            uA = self.lineEdit_2.text()
            qty = self.lineEdit_3.text()
            #print(mode)
      
        
        #data = [[mode,kV,uA,timeOut]]
        


        with open('data\\log\\XRay_Monitoring.csv', 'r') as f:
            reader = csv.DictReader(f, delimiter=',')
            # All rows
            rows = list(reader)
            # Update last row
            rows[-1].update({'TimeOut': timeOut, 'Mode': mode, 'Voltage': kV, 'Current': uA, 'NoOfUnits': qty})

        with open('data\\log\\XRay_Monitoring.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames = rows[-1].keys())
            writer.writeheader()
            writer.writerows(rows)


        #print(mode)
        with open('data\\log\\superlog.txt', 'a') as f:
            print(mode, file=f)
            print('Time-out', timeOut, '\n', file=f)
            f.close()

        #sys.stdout.close()
    
           
    #def ret_Home(self, checked):
    def ret_Home(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        #self.kill()        
        self.w = MainWindow()
        self.w.showFullScreen()
        self.kill()

    def get_timeOut(self):
        global timeOut
        now=datetime.now()
        timeOut=now.strftime("%m/%d/%Y %H:%M:%S")        

    def kill(self):
        self.destroy()
  

import icons_rc

class MainWindow(QMainWindow):
#class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.launchUi()
        self._want_to_close = False

    def closeEvent(self, evnt):
        if self._want_to_close:
            QtGui.QWidget.closeEvent(evnt)
        else:
            evnt.ignore()
            #self.setWindowState(QtCore.Qt.WindowMinimized)

    def launchUi(self):
        
        self.setWindowTitle("aXiS (c) jcsaludares")
        self.setWindowIcon(QtGui.QIcon('ui\\xray_150x150.png'))
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        #print(screen)

        #layout = QFormLayout()
        #layout.addRow("Name:", QLineEdit())
        #self.setLayout(layout)       

        
        #widget_origin_w = int((labelRectW + lineRectW + 10)/2)

        oImage = QImage('ui\\image2.jpg')        
        #sImage = oImage.scaled(QSize(320,240))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(oImage))                        
        self.setPalette(palette)
    

        self.userLabel = QLabel(self)
        self.userLabel.setText("Tap ID Card")
        self.userLabel.setFont(QFont('Tw Cen MT', 22))
        self.userLabel.setStyleSheet("color: white")
        self.userLabel.setGeometry((int(screen.width()/2 - Whole_Line_H/2)),int(screen.height()/2),Label_W,Label_H)
        
        #self.userLabel.setAlignment(Qt.AlignRight)

        #print("Label_W=", self.userLabel.width())
        #print("LabelRectWidth=", self.userLabel.fontMetrics().boundingRect(self.userLabel.text()).width())
        #print("Label_H=", self.userLabel.height())
        #print("LabelRectHeight=", self.userLabel.fontMetrics().boundingRect(self.userLabel.text()).height())

        self.userRFID = QLineEdit(self)        
        self.userRFID.setGeometry(int(screen.width()/2 - Whole_Line_H/2+Label_W+widget_gap_W), int(screen.height()/2),Line_W,Line_H)
        self.userRFID.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 0)")
        self.userRFID.setFont(QFont('Arial', 17))
        self.userRFID.setAlignment(Qt.AlignCenter)
        self.userRFID.setEchoMode(QtWidgets.QLineEdit.Password)
        #self.userRFID.setAlignment(Qt.AlignRight)
        self.userRFID.returnPressed.connect(self.rfidDetected)
        #print("RFID: ", self.userRFID.width())

        #print("Line_W=", self.userRFID.width())
        #print("LineRectWidth=", self.userRFID.fontMetrics().boundingRect(self.userLabel.text()).width())
        #print("Line_H=", self.userRFID.height())
        #print("LineRectHeight=", self.userRFID.fontMetrics().boundingRect(self.userLabel.text()).height())

        self.newUser = QCommandLinkButton("New User", self)
        self.newUser.setGeometry(int(screen.width()/2 - Whole_Line_H/2+Label_W+widget_gap_W), int(screen.height()/2)+ Line_H + widget_gap_H,NewUser_W,NewUser_H)
        self.newUser.clicked.connect(self.show_new_window)
        #print("NewUser: ", self.newUser.width())

        #print("NewUser_W=", self.newUser.width())
        #print("NewUserRectWidth=", self.newUser.fontMetrics().boundingRect(self.userLabel.text()).width())
        #print("NewUser_H=", self.newUser.height())
        #print("NewUserRectHeight=", self.newUser.fontMetrics().boundingRect(self.userLabel.text()).height())
        
        self.label_time = QLabel(self)
        self.label_time.setGeometry(screen.width()- label_time_W - screen_W_allowance-adj_W, screen_H_allowance, label_time_W, label_time_H)
        self.label_time.setStyleSheet('color:white; font-size: 60pt; font-family: Tw Cen MT Condensed;')

        #print("label_time_W=", self.label_time.width())
        #print("label_timeRectW=", self.label_time.fontMetrics().boundingRect(self.label_time.text()).width())
        #print("label_time_H=", self.label_time.height())
        #print("label_timeRectH=", self.label_time.fontMetrics().boundingRect(self.label_time.text()).height())
        
        self.label_date = QLabel(self)
        self.label_date.setGeometry(screen.width()- label_date_W - screen_W_allowance-adj_W, screen_W_allowance + label_time_H + widget_gap_H, label_date_W, label_date_H)
        self.label_date.setStyleSheet('color:white; font-size: 18pt; font-family: Tw Cen MT;')

        #print("label_date_W=", self.label_date.width())
        #print("label_dateRectW=", self.label_date.fontMetrics().boundingRect(self.label_date.text()).width())
        #print("label_date_H=", self.label_date.height())
        #print("label_dateRectH=", self.label_date.fontMetrics().boundingRect(self.label_date.text()).height())
        
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.displayTime)
        self.timer.timeout.connect(self.displayDate)
        self.timer.start()        

        self.userRFID.setFocus()
        #self.showFullScreen()

        self.build_dict()
        self.build_owners() 

    def displayTime(self):
        self.label_time.setText(QtCore.QTime.currentTime().toString())

    def displayDate(self):
        self.label_date.setText(QtCore.QDate.currentDate().toString())

    def show_new_window(self, checked):
        #self.w = AddUser()
        #self.w.show()
        msgBox = QMessageBox(QMessageBox.Information,"aXiS","To register, please contact admin",parent=self,)            
        msgBox.setWindowIcon(QtGui.QIcon('ui\\xray_150x150.png'))
        #msgBox.setStyleSheet("background-color: rgb(0, 0, 0);")
        msgBox.setStyleSheet("QLabel{ color: rgb(0, 0, 0)}")
        msgBox.setFont(QFont('Bahnschrift', 14))
        msgBox.exec_()
        #self.kill()

    def show_logOut(self):
        #self.showNormal()
        #self.hide()
        self.w = LogOut()
        self.w.show()

    def kill(self):
        self.destroy()

    def build_dict(self):
        global user_repo
        with open('data\\admin\\userlist.csv', mode ='r') as infile:
            reader = csv.reader(infile)
            with open('data\\temp\\userlist_new.csv', mode = 'w') as outfile:
                writer = csv.writer(outfile)
                user_repo = {rows[1]:rows[0] for rows in reader}
                outfile.close()
            infile.close()

    def build_owners(self):
        global owners_repo
        with open('data\\admin\\ownerlist.csv', mode ='r') as infile:
            reader = csv.reader(infile)
            with open('data\\temp\\ownerlist_new.csv', mode = 'w') as outfile:
                writer = csv.writer(outfile)
                owners_repo = {rows[1]:rows[0] for rows in reader}
                outfile.close()
            infile.close()

    def get_time(self):
        global timeIn
        now=datetime.now()
        timeIn=now.strftime("%m/%d/%Y %H:%M:%S")
          
    def rfidDetected(self):
        global rfidTag
        rfidTag=self.userRFID.text()
        #print (rfidTag)
        self.userRFID.clear()
        self.get_time()        
        
        if rfidTag not in user_repo:
        
            with open('data\\log\\XRay_Monitoring.csv', 'a',newline='') as fp:
                file = csv.writer(fp, delimiter=',')
                data = [[rfidTag, 'Unknown User', timeIn]]
                file.writerows(data)
                fp.close()

            with open('data\\log\\superlog.txt', 'a') as f:                    
                print ("Unknown User:", rfidTag, file=f)
                print ("Time-in: ", timeIn, '\n', file=f)
                f.close()
            
            msgBox = QMessageBox(QMessageBox.Information,"aXiS","User not recognized, please contact admin",parent=self,)            
            msgBox.setWindowIcon(QtGui.QIcon('ui\\xray_150x150.png'))
            #msgBox.setStyleSheet("background-color: rgb(0, 0, 0);")
            msgBox.setStyleSheet("QLabel{ color: rgb(0, 0, 0)}")
            msgBox.setFont(QFont('Bahnschrift', 14))
            msgBox.exec_()
            
        else:
            #fname = user_repo[rfidTag].split() [0]
            fname = user_repo[rfidTag]
            with open('data\\log\\XRay_Monitoring.csv', 'a',newline='') as fp:
                file = csv.writer(fp, delimiter=',')
                data = [[rfidTag,fname,timeIn]]
                file.writerows(data)
                fp.close()
                
            with open('data\\log\\superlog.txt', 'a') as f:
                print ("User: ",fname, file=f)
                print ("Time-in: ", timeIn, file=f)
                f.close()
            #self.kill()
            self.show_logOut()
            self.kill()


app = QApplication(sys.argv)
w = MainWindow()
w.showFullScreen()
app.exec()
