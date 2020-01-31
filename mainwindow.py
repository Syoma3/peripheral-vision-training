from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi_main(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(292, 261)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(60, 10, 171, 71))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.start.setFont(font)
        self.start.setObjectName("start")
        self.stats = QtWidgets.QPushButton(self.centralwidget)
        self.stats.setGeometry(QtCore.QRect(60, 90, 171, 71))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.stats.setFont(font)
        self.stats.setObjectName("stats")
        self.exit = QtWidgets.QPushButton(self.centralwidget)
        self.exit.setGeometry(QtCore.QRect(60, 170, 171, 71))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.exit.setFont(font)
        self.exit.setObjectName("exit")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start.setText(_translate("MainWindow", "Начать"))
        self.stats.setText(_translate("MainWindow", "Статистика"))
        self.exit.setText(_translate("MainWindow", "Выход"))
