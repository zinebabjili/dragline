import datetime
import sqlite3
from threading import Event

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QLineEdit, QLabel, QWidget, QMessageBox

from PyQt5 import QtWidgets, QtCore

from controllers.loginCtrl import LoginCtrl
from controllers.timeCtrl import Controller
from db.draglineDb import get_emps_by_password
from gui.dragline import Dragline
from gui.stylesheet import stylesheet


class Login(object):
    def setupUi(self, MainWindow):

        # Button text | position on the QGridLayout
        self.buttons = {'1': (0, 0),
                        '2': (0, 1),
                        '3': (0, 2),
                        '4': (1, 0),
                        '5': (1, 1),
                        '6': (1, 2),
                        '7': (2, 0),
                        '8': (2, 1),
                        '9': (2, 2),
                        '0': (3, 1),
                        'x': (3, 2),
                        }

        # MainWindow.resize(860, 600)

        self.vBox = QVBoxLayout(MainWindow)
        self.vBox.setSpacing(0)
        self.vBox.setContentsMargins(0, 0, 0, 0)

        """header title"""

        self.titleWidget = QWidget()
        self.titleWidget.setObjectName("titleWidget")

        self.hBox = QHBoxLayout()
        self.titleWidget.setLayout(self.hBox)

        self.vBox.addWidget(self.titleWidget, 5)

        self.widgetLeftTitle = QWidget()
        self.hBox.addWidget(self.widgetLeftTitle)

        self.lblBigTitle = QLabel()
        self.lblBigTitle.setText("Dragline Dashboard")
        self.lblBigTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lblBigTitle.setObjectName("lblBigTitle")

        self.hBox.addWidget(self.lblBigTitle)

        self.imgPillioty = QLabel()
        self.pixmapPillioty = QPixmap('../images/pillioty logo.png')
        self.pixmapSizePillioty = self.pixmapPillioty.scaled(100, 100, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.imgPillioty.setAlignment(QtCore.Qt.AlignRight)
        self.imgPillioty.setPixmap(self.pixmapSizePillioty)

        self.hBox.addWidget(self.imgPillioty)

        """header dragline information"""

        self.infoWidget = QWidget()
        self.infoWidget.setObjectName("infowidget")

        self.hBoxDraglineInfo = QHBoxLayout()
        self.infoWidget.setLayout(self.hBoxDraglineInfo)

        self.vBox.addWidget(self.infoWidget, 5)

        self.gridLayout1 = QGridLayout()
        self.hBoxDraglineInfo.addLayout(self.gridLayout1)

        self.lblDraglineId = QLabel()
        self.lblDraglineId.setText("ID Dragline:")
        self.gridLayout1.addWidget(self.lblDraglineId, 1, 0)

        self.lblDate = QLabel()
        self.lblDate.setText("Date :")
        self.gridLayout1.addWidget(self.lblDate, 2, 0)

        self.date = QLabel()
        self.date.setText((str)(datetime.date.today()))
        self.gridLayout1.addWidget(self.date, 2, 1)

        self.lblTime = QLabel()
        self.lblTime.setText("Time :")
        self.gridLayout1.addWidget(self.lblTime, 3, 0)

        self.stop_flag_time = Event()
        self.getController = Controller(self.stop_flag_time)
        self.getController.start()
        self.getController.newTime.connect(self.updateTime)

        self.time = QLabel()
        self.gridLayout1.addWidget(self.time, 3, 1)

        self.widgetRight = QWidget()
        self.hBoxDraglineInfo.addWidget(self.widgetRight, 50)

        """Body"""
        self.hBody = QHBoxLayout()
        self.widgetBody = QWidget()
        self.widgetBody.setObjectName("bodyWidget")
        self.widgetBody.setLayout(self.hBody)
        self.vBox.addWidget(self.widgetBody, 50)

        self.vBoxImage = QVBoxLayout()
        self.hBody.addLayout(self.vBoxImage)

        self.lblimgOCP = QLabel()
        self.pixmap = QPixmap('../images/logo ocp.png')
        self.lblimgOCP.setPixmap(self.pixmap)
        self.vBoxImage.addWidget(self.lblimgOCP)

        self.vBoxLogin = QVBoxLayout()
        self.hBody.addLayout(self.vBoxLogin)

        self.display = QLineEdit()
        self.display.setFocus()
        # self.display.setAlignment(QtCore.Qt.AlignCenter)
        self.display.setPlaceholderText("ID Conducteur")
        self.display.setFixedWidth(500)
        self.display.setFixedHeight(40)
        self.display.setEchoMode(QLineEdit.Password)
        self.display.setMaxLength(4)
        self.vBoxLogin.addWidget(self.display, alignment=QtCore.Qt.AlignCenter)

        self.gridWidget = QWidget()
        self.gridWidget.setFixedWidth(500)
        self.gridWidget.setFixedHeight(300)
        self.gridWidget.setObjectName("gridWidget")
        self.vBoxLogin.addWidget(self.gridWidget, alignment=QtCore.Qt.AlignCenter)
        self.buttonsLayout = QGridLayout(self.gridWidget)

        # Create the buttons and add them to the grid layout
        for btnText, pos in self.buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setObjectName("btn")
            self.buttons[btnText].setFixedSize(50, 40)
            self.buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])

        self.vBoxLogin.addLayout(self.buttonsLayout)

        self.buttonValider = QPushButton('Valider')
        self.buttonValider.setFixedHeight(30)
        self.buttonValider.setFixedWidth(130)
        self.buttonValider.setObjectName("btn")
        self.vBoxLogin.addWidget(self.buttonValider, alignment=QtCore.Qt.AlignCenter)
        self.buttonValider.clicked.connect(self.changePage)

    def setDisplayText(self, text):
        """Set display's text."""
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        """Get display's text."""
        return self.display.text()

    def clearDisplay(self):
        """Clear the display."""
        self.setDisplayText('')

    def changePage(self):
        self.data = get_emps_by_password(str(self.displayText()))
        if self.data != None:
            self.display.setText('')
            window.hide()
            self.window = QtWidgets.QWidget()
            self.ui = Dragline(data=self.data)
            self.ui.setupUi(self.window)
            self.window.show()
            self.ui.startTimer()
        else:
            QMessageBox.critical(window, "Error", 'No Account With That Password')

    def updateTime(self, timeInterval):
        self.time.setText(timeInterval)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    app.setStyleSheet(stylesheet)
    ui = Login()
    ui.setupUi(window)
    # Create instances of the model and the controller
    LoginCtrl(view=ui)
    window.show()
    sys.exit(app.exec_())
