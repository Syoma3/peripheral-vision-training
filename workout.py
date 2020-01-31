import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QInputDialog, QPushButton, QMessageBox, QLabel
from mainwindow import Ui_MainWindow
from game import Ui_Form_Game
from random import sample
from PyQt5.QtCore import QTimer
from result import Ui_Form_Result
import sqlite3
import pyqtgraph
from PyQt5.Qt import QVBoxLayout


def made_set_n():
    a = list(range(1, 26))
    a = sample(a, 25)
    k = 0
    b = []
    lst_n = []
    for i in range(5):
        for j in range(5):
            b.append(a[k])
            k += 1
        lst_n.append(b)
        b = []
    return lst_n


def search(element, matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == element:
                return [i, j]


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi_main(self)
        self.start.clicked.connect(self.choice_mode)
        self.stats.clicked.connect(self.start_plot)
        self.exit.clicked.connect(self.exit_)

    def choice_mode(self):
        i, okBtn = QInputDialog.getItem(self, 'Выберите сложность.', '', ('easy', 'medium', 'hard'), 1, False)
        if okBtn:
            self.game = Game(i)
            self.game.show()

    def start_plot(self):
        i, okBtn = QInputDialog.getItem(self, 'Выберите сложность.', '', ('easy', 'medium', 'hard'), 1, False)
        if okBtn:
            self.pt = Plot(i)
            self.pt.show()

    def exit_(self):
        self.close()


class Game(QWidget, Ui_Form_Game):
    def __init__(self, arg):
        super().__init__()
        self.setupUi_game(self)
        self.mode = arg
        self.SetPbn = [[self.pbn_1, self.pbn_2, self.pbn_3, self.pbn_4, self.pbn_5],
                       [self.pbn_6, self.pbn_7, self.pbn_8, self.pbn_9, self.pbn_10],
                       [self.pbn_11, self.pbn_12, self.pbn_13, self.pbn_14, self.pbn_15],
                       [self.pbn_16, self.pbn_17, self.pbn_18, self.pbn_19, self.pbn_20],
                       [self.pbn_21, self.pbn_22, self.pbn_23, self.pbn_24, self.pbn_25]]
        self.setupUi()

    def setupUi(self):
        self.pbn.clicked.connect(self.game)

    def game(self):
        self.flag = True
        self.made_set_pbn()
        self.number = 1
        self.time = 0
        self.label_press.setText(f'Нажмите на {self.number}')
        self.timer = QTimer()
        self.timer.timeout.connect(self.timePlus)
        self.timer.start(1000)
        for i in self.SetPbn:
            for j in i:
                j.clicked.connect(self.check_press)

    def made_set_pbn(self):
        self.lst_n = made_set_n()
        for i in range(5):
            for j in range(5):
                self.SetPbn[i][j].setText(str(self.lst_n[i][j]))
                self.SetPbn[i][j].setStyleSheet('''background-color: white;''')

    def check_press(self):
        sender = self.sender()
        i, j = search(self.number, self.lst_n)
        if int(sender.text()) == self.lst_n[i][j] and self.flag:
            if self.number != 25:
                self.number += 1
                self.label_press.setText(f'Нажмите на {str(self.number)}')
                if self.mode == 'easy':
                    sender.setStyleSheet('''background-color: gray;''')
                elif self.mode == 'hard':
                    self.made_set_pbn()
            else:
                self.flag = False
                self.timer.stop()
                self.r = Result(self.time, self.mode)
                self.r.show()
                self.pbn.setText('Заново')
                con = sqlite3.connect('statistics.db')
                cur = con.cursor()
                if self.mode == 'hard':
                    m = 3
                elif self.mode == 'medium':
                    m = 2
                else:
                    m = 1
                cur.execute("""INSERT INTO result(mode, time) VALUES(?, ?)""",
                            (m, self.time))
                con.commit()
                con.close()
                self.pbn.clicked.connect(self.game)

    def timePlus(self):
        self.time += 1
        self.label_time.setText(f'Время: {self.time} с')


class Result(Ui_Form_Result, QWidget):
    def __init__(self, time, mode):
        super().__init__()
        self.setupUi_result(self)
        self.label_2.setText(f'Ваш результат: {time} c')
        self.label_3.setText(f'режим: {mode}')


class Plot(QWidget):
    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        self.con = sqlite3.connect('statistics.db')
        window = QVBoxLayout(self)
        self.view = pyqtgraph.PlotWidget()
        self.chart = self.view.plot(name='time_from_kol-va')
        cur = self.con.cursor()
        k = cur.execute("""SELECT time from result 
                                                WHERE mode IN (
                                                SELECT id from modes
                                                WHERE title = ?)""", (self.mode,)).fetchall()
        self.chart.setData(list(range(1, len(k) + 1)), [x[0] for x in k])
        self.pbn = QPushButton('Удалить все данные')
        self.pbn.clicked.connect(self.delete_info)
        self.label = QLabel('График зависимости времени от кол-ва игр.')
        window.addWidget(self.label)
        window.addWidget(self.view)
        window.addWidget(self.pbn)

    def delete_info(self):
        valid = QMessageBox.question(self, 'Удаление статистики',
                                     'Вы действительно хотите удалить статистику?', QMessageBox.Yes, QMessageBox.No)
        if valid:
            cur = self.con.cursor()
            cur.execute("""DELETE from result
                                WHERE mode IN (
                                SELECT id from modes
                                    WHERE title = ?)""", (self.mode,))
            self.con.commit()


app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec_())