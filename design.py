# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Design.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(537, 206)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.CBWar2 = QtWidgets.QComboBox(self.centralwidget)
        self.CBWar2.setObjectName("CBWar2")
        self.gridLayout.addWidget(self.CBWar2, 2, 1, 1, 1)
        self.BtnLoad = QtWidgets.QPushButton(self.centralwidget)
        self.BtnLoad.setObjectName("BtnLoad")
        self.gridLayout.addWidget(self.BtnLoad, 1, 9, 1, 1)
        self.LblWar2 = QtWidgets.QLabel(self.centralwidget)
        self.LblWar2.setObjectName("LblWar2")
        self.gridLayout.addWidget(self.LblWar2, 2, 3, 1, 1, QtCore.Qt.AlignRight)
        self.LblWar1 = QtWidgets.QLabel(self.centralwidget)
        self.LblWar1.setObjectName("LblWar1")
        self.gridLayout.addWidget(self.LblWar1, 2, 0, 1, 1)
        self.BtnFight = QtWidgets.QPushButton(self.centralwidget)
        self.BtnFight.setEnabled(False)
        self.BtnFight.setObjectName("BtnFight")
        self.gridLayout.addWidget(self.BtnFight, 2, 9, 1, 1)
        self.LblWar1Vik = QtWidgets.QLabel(self.centralwidget)
        self.LblWar1Vik.setObjectName("LblWar1Vik")
        self.gridLayout.addWidget(self.LblWar1Vik, 6, 0, 1, 2)
        self.LblHits = QtWidgets.QLabel(self.centralwidget)
        self.LblHits.setObjectName("LblHits")
        self.gridLayout.addWidget(self.LblHits, 3, 0, 1, 2)
        self.LblWa2Wound = QtWidgets.QLabel(self.centralwidget)
        self.LblWa2Wound.setObjectName("LblWa2Wound")
        self.gridLayout.addWidget(self.LblWa2Wound, 7, 3, 1, 2)
        self.LblWar1Wounds = QtWidgets.QLabel(self.centralwidget)
        self.LblWar1Wounds.setObjectName("LblWar1Wounds")
        self.gridLayout.addWidget(self.LblWar1Wounds, 6, 2, 1, 3)
        self.LblWar2Vik = QtWidgets.QLabel(self.centralwidget)
        self.LblWar2Vik.setObjectName("LblWar2Vik")
        self.gridLayout.addWidget(self.LblWar2Vik, 7, 0, 1, 2)
        self.LblWords = QtWidgets.QLabel(self.centralwidget)
        self.LblWords.setObjectName("LblWords")
        self.gridLayout.addWidget(self.LblWords, 3, 2, 1, 4)
        self.CB2 = QtWidgets.QComboBox(self.centralwidget)
        self.CB2.setObjectName("CB2")
        self.gridLayout.addWidget(self.CB2, 2, 4, 1, 2)
        self.SpinNum = QtWidgets.QSpinBox(self.centralwidget)
        self.SpinNum.setMinimum(1)
        self.SpinNum.setMaximum(100)
        self.SpinNum.setProperty("value", 50)
        self.SpinNum.setObjectName("SpinNum")
        self.gridLayout.addWidget(self.SpinNum, 2, 7, 1, 2)
        self.LblWar1Tired = QtWidgets.QLabel(self.centralwidget)
        self.LblWar1Tired.setObjectName("LblWar1Tired")
        self.gridLayout.addWidget(self.LblWar1Tired, 6, 6, 1, 1)
        self.LblNum = QtWidgets.QLabel(self.centralwidget)
        self.LblNum.setObjectName("LblNum")
        self.gridLayout.addWidget(self.LblNum, 2, 6, 1, 1)
        self.LblWar2Tired = QtWidgets.QLabel(self.centralwidget)
        self.LblWar2Tired.setObjectName("LblWar2Tired")
        self.gridLayout.addWidget(self.LblWar2Tired, 7, 6, 1, 1)
        self.LblWar1Kern = QtWidgets.QLabel(self.centralwidget)
        self.LblWar1Kern.setObjectName("LblWar1Kern")
        self.gridLayout.addWidget(self.LblWar1Kern, 6, 7, 1, 1)
        self.LblWar2Kern = QtWidgets.QLabel(self.centralwidget)
        self.LblWar2Kern.setObjectName("LblWar2Kern")
        self.gridLayout.addWidget(self.LblWar2Kern, 7, 7, 1, 1)
        self.LblEnd = QtWidgets.QLabel(self.centralwidget)
        self.LblEnd.setObjectName("LblEnd")
        self.gridLayout.addWidget(self.LblEnd, 0, 8, 1, 1)
        self.LblStart = QtWidgets.QLabel(self.centralwidget)
        self.LblStart.setObjectName("LblStart")
        self.gridLayout.addWidget(self.LblStart, 0, 7, 1, 1)
        self.TxtPath = QtWidgets.QLineEdit(self.centralwidget)
        self.TxtPath.setObjectName("TxtPath")
        self.gridLayout.addWidget(self.TxtPath, 1, 0, 1, 7)
        self.LblPath = QtWidgets.QLabel(self.centralwidget)
        self.LblPath.setObjectName("LblPath")
        self.gridLayout.addWidget(self.LblPath, 0, 0, 1, 1)
        self.LineStart = QtWidgets.QLineEdit(self.centralwidget)
        self.LineStart.setObjectName("LineStart")
        self.gridLayout.addWidget(self.LineStart, 1, 7, 1, 1)
        self.LineEnd = QtWidgets.QLineEdit(self.centralwidget)
        self.LineEnd.setInputMask("")
        self.LineEnd.setObjectName("LineEnd")
        self.gridLayout.addWidget(self.LineEnd, 1, 8, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 537, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Проверка вероятностей"))
        self.BtnLoad.setText(_translate("MainWindow", "Загрузить"))
        self.LblWar2.setText(_translate("MainWindow", "Воин2"))
        self.LblWar1.setText(_translate("MainWindow", "Воин1"))
        self.BtnFight.setText(_translate("MainWindow", "Сразиться"))
        self.LblWar1Vik.setText(_translate("MainWindow", "Воин1 победил "))
        self.LblHits.setText(_translate("MainWindow", "Число ударов"))
        self.LblWa2Wound.setText(_translate("MainWindow", "Из них ранения:"))
        self.LblWar1Wounds.setText(_translate("MainWindow", "Из них ранения:"))
        self.LblWar2Vik.setText(_translate("MainWindow", "Воин2 победил"))
        self.LblWords.setText(_translate("MainWindow", "Число слов"))
        self.LblWar1Tired.setText(_translate("MainWindow", "Вымотал"))
        self.LblNum.setText(_translate("MainWindow", "Число сражений"))
        self.LblWar2Tired.setText(_translate("MainWindow", "Вымотал"))
        self.LblWar1Kern.setText(_translate("MainWindow", "Ядро"))
        self.LblWar2Kern.setText(_translate("MainWindow", "Ядро"))
        self.LblEnd.setText(_translate("MainWindow", "Низ справа"))
        self.LblStart.setText(_translate("MainWindow", "Верх слева"))
        self.LblPath.setText(_translate("MainWindow", "URL"))
        self.LineStart.setText(_translate("MainWindow", "a2"))
        self.LineEnd.setText(_translate("MainWindow", "k19"))

