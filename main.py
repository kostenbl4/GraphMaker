import sqlite3
import sys
from math import *
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib import pyplot as plt

from graph_maker_new import Ui_MainWindow  # импорт дизайна окна ввода данных
from info_widget import Ui_Form  # импорт дизайна окна инструкции


# класс окна ввода данных
class InputWindow(QMainWindow, Ui_MainWindow):
    # конструктор
    def __init__(self):
        super(InputWindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(520, 509)
        self.add_func()
        self.theme = 'DARK'
        # коннект слотов к виджетам
        self.info_btn.clicked.connect(self.show_info)

        self.makegraph_btn.clicked.connect(self.PlotGraph)

        self.makegraph_btn.clicked.connect(self.add_func)

        self.theme_btn.clicked.connect(self.changeTheme)

    # создание экземпляра класса InfoWindow() и его высвечивание на экран
    def show_info(self):
        self.info = InfoWindow()
        self.info.show()

    # метод для кнопок с галочкой в правом списке функций, который меняет ввод функции
    def change_input_func(self):

        self.func_input.setText(self.sender().button_fun)

    # метод для кнопок с крестиком в правом списке функций, который удаляет функцию из этого
    # списка(и из БД)
    def del_func(self):

        con = sqlite3.connect('MyDB.db')
        cur = con.cursor()

        cur.execute('DELETE from func_table WHERE id = ?', (self.sender().id,)).fetchall()

        con.commit()
        con.close()
        self.update_funcs()

    # метод, обновляющий список функций
    def update_funcs(self):
        con = sqlite3.connect('MyDB.db')
        cur = con.cursor()

        result = cur.execute('SELECT * from func_table').fetchall()

        self.layout = QFormLayout(self)
        self.groupBox = QGroupBox()

        self.list_label = []
        self.list_button = []
        self.list_del_button = []
        self.funcs_list = []

        num = 0

        hlayout = QGridLayout(self)

        for elem in result:

            id = elem[0]
            function = elem[1]

            if function != '':
                if 'x' in function and 'y' in function:
                    self.list_label.append(QLabel("‣ {}".format(function)))
                    self.list_button.append(QPushButton('✔'))
                    self.list_del_button.append(QPushButton('✖'))
                    self.funcs_list.append(function)

                    self.list_button[num].button_fun = function
                    self.list_del_button[num].id = id
                    self.list_del_button[num].num = num

                    hlayout.addWidget(self.list_label[num], num, 0)
                    hlayout.addWidget(self.list_button[num], num, 1)
                    hlayout.addWidget(self.list_del_button[num], num, 2)

                    self.list_button[num].clicked.connect(self.change_input_func)
                    self.list_del_button[num].clicked.connect(self.del_func)

                    self.list_label[num].setFont(QFont("Montserrat Medium", 14, QFont.Bold))

                    num += 1
                else:
                    self.statusbar.showMessage('���ОШИБКА ВВОДА���')

        self.layout.addRow(hlayout)
        self.groupBox.setLayout(self.layout)
        self.scrollArea.setWidget(self.groupBox)

        con.commit()
        con.close()

    # метод, добавляющий новую функцию в БД и список
    def add_func(self):

        con = sqlite3.connect('MyDB.db')
        cur = con.cursor()

        if self.func_input.text() != '':
            if 'x' in self.func_input.text() and 'y' in self.func_input.text():
                if all(list(map(lambda x: x.isdigit, self.range_input.text()))) and \
                        all(list(map(lambda x: x.isdigit, self.step_input.text()))):
                    cur.execute('INSERT INTO func_table(FUNC) VALUES(?)',
                                (self.func_input.text().replace(' ', '').lower(),)).fetchall()

        result = cur.execute('SELECT * from func_table').fetchall()

        self.layout = QFormLayout(self)
        self.groupBox = QGroupBox()

        self.list_label = []
        self.list_button = []
        self.list_del_button = []
        self.funcs_list = []

        num = 0

        hlayout = QGridLayout(self)

        for elem in result:

            id = elem[0]
            function = elem[1]

            if function != '':
                if 'x' in function and 'y' in function:
                    self.list_label.append(QLabel("‣ {}".format(function)))
                    self.list_button.append(QPushButton('✔'))
                    self.list_del_button.append(QPushButton('✖'))
                    self.funcs_list.append(function)

                    self.list_button[num].button_fun = function
                    self.list_del_button[num].id = id
                    self.list_del_button[num].num = num

                    hlayout.addWidget(self.list_label[num], num, 0)
                    hlayout.addWidget(self.list_button[num], num, 1)
                    hlayout.addWidget(self.list_del_button[num], num, 2)

                    self.list_button[num].clicked.connect(self.change_input_func)
                    self.list_del_button[num].clicked.connect(self.del_func)

                    self.list_label[num].setFont(QFont("Montserrat Medium", 14, QFont.Bold))

                    num += 1

        self.layout.addRow(hlayout)
        self.groupBox.setLayout(self.layout)
        self.scrollArea.setWidget(self.groupBox)

        con.commit()
        con.close()

    # метод, изменяющий цветовую тему окна ввода данных
    def changeTheme(self):

        if self.theme == 'LIGHT':
            self.frame.setStyleSheet("background-color: #4a536b;""")
            self.range_input.setStyleSheet("background-color: #ff9a8d;\n"
                                           "border: 2px solid  #aed6dc;\n"
                                           "border-radius: 20px;")
            self.func_input.setStyleSheet("background-color: #ff9a8d;\n"
                                          "border: 2px solid  #aed6dc;\n"
                                          "border-radius: 20px;")
            self.step_input.setStyleSheet("background-color: #ff9a8d;\n"
                                          "border: 2px solid  #aed6dc;\n"
                                          "border-radius: 20px;")
            self.label.setStyleSheet("color: #aed6dc")
            self.makegraph_btn.setStyleSheet("color: #525252;\n"
                                             "background-color:#aed6dc\n"
                                             "")
            icon2 = QIcon()
            icon2.addPixmap(QPixmap("Light_Theme-512.png"), QIcon.Normal, QIcon.Off)
            self.theme_btn.setIcon(icon2)
            self.theme_btn.setStyleSheet("background-color: #ff9a8d;\n"
                                         "border-radius: 15px;\n"
                                         "border: 2px solid  rgb(174, 214, 220);")
            self.info_btn.setStyleSheet("background-color: #ff9a8d;\n"
                                        "border-radius: 15px;\n"
                                        "border: 2px solid  #aed6dc;")
            self.scrollArea.setStyleSheet("background-color: #aed6dc;")

            self.theme = 'DARK'

            return

        elif self.theme == 'DARK':
            self.frame.setStyleSheet("background-color: #c6d7eb;""")
            self.range_input.setStyleSheet("background-color: #fbcbc9;\n"
                                           "border: 2px solid  #4a536b;\n"
                                           "border-radius: 20px;")
            self.func_input.setStyleSheet("background-color: #fbcbc9;\n"
                                          "border: 2px solid  #4a536b;\n"
                                          "border-radius: 20px;")
            self.step_input.setStyleSheet("background-color: #fbcbc9;\n"
                                          "border: 2px solid  #4a536b;\n"
                                          "border-radius: 20px;")
            self.label.setStyleSheet("color: #1e3d59")
            self.makegraph_btn.setStyleSheet("color: #aed6dc;\n"
                                             "background-color:#1e3d59\n"
                                             "")
            icon2 = QIcon()
            icon2.addPixmap(QPixmap("Dark_Theme-512.png"), QIcon.Normal, QIcon.Off)
            self.theme_btn.setIcon(icon2)
            self.theme_btn.setStyleSheet("background-color: #fbcbc9;\n"
                                         "border-radius: 15px;\n"
                                         "border: 2px solid  #4a536b;")
            self.info_btn.setStyleSheet("background-color: #fbcbc9;\n"
                                        "border-radius: 15px;\n"
                                        "border: 2px solid  #4a536b;")
            self.scrollArea.setStyleSheet("background-color: #1e3d59;")

            self.theme = 'LIGHT'

            return

    # метод, выводящий окно с готовым графиком
    def PlotGraph(self):

        if self.func_input.text() == '':
            self.statusbar.showMessage('���ВЫ НЕ ВВЕЛИ ФУНЦИЮ���')

            return

        # функция, которая чертит гроафик по готовым спискам иксов и игриков
        def plot_func():

            for ytuple in ylist:
                if list(ytuple)[1] is None:
                    del ylist[list(ytuple)[0]]
                    del xlist[list(ytuple)[0]]

            main_xlist = list(map(lambda x: x[1], xlist))
            main_ylist = list(map(lambda x: x[1], ylist))

            plt.plot(main_xlist, main_ylist, color='#aed6dc')
            plt.grid()
            plt.title(f'График {self.func_input.text().lower()}')
            plt.show()

        # функция, которая возвращает список иксов, исходя из вводных данных
        def make_xlist(xmin, xmax, stepx):

            if xmin == '' and xmax == '' and stepx == '':
                xlist = np.around(np.arange(-20, 20, 0.1), decimals=4)
                return list(xlist)

            elif xmin == '' and xmax != '' and stepx != '':
                xlist = np.around(np.arange(-20, int(xmax), int(stepx)), decimals=4)
                return list(xlist)

            elif xmin == '' and xmax == '' and stepx != '':
                xlist = np.around(np.arange(-20, 20, int(stepx)), decimals=4)
                return list(xlist)

            elif xmin != '' and xmax == '' and stepx != '':
                xlist = np.around(np.arange(int(xmin), 20, int(stepx)), decimals=4)
                return list(xlist)

            elif xmin != '' and xmax != '' and stepx == '':
                xlist = np.around(np.arange(int(xmin), int(xmax), 0.1), decimals=4)
                return list(xlist)

            elif xmin == '' and xmax != '' and stepx == '':
                xlist = np.around(np.arange(-20, int(xmax), 0.1), decimals=4)
                return list(xlist)

            else:
                xlist = np.around(np.arange(int(xmin), int(xmax), int(stepx)), decimals=4)

                return list(xlist)

        # функция - оболочка, которая обрабатывает поступающий ей на вход 'x', исходя из ввода
        def make_ylist(x):
            try:
                return eval(
                    self.func_input.text().strip().lower().replace('y', '')
                        .replace('=', '').replace('x', '(x)').replace('x', str(x)))


            except Exception:

                return None

        # тут рассматриваются случаи с разным вводом данных
        try:
            if self.range_input.text() == '' and self.step_input.text() == '':

                xmin = ''
                xmax = ''
                stepx = ''
                xlist = list(enumerate(make_xlist(xmin, xmax, stepx)))

                ylist = list(map(lambda x: [x[0], make_ylist(x[1])], xlist))

                plot_func()
            elif self.range_input.text() == '' and self.step_input.text() != '':
                xmin = ''
                xmax = ''
                stepx = self.step_input.text()
                xlist = list(enumerate(make_xlist(xmin, xmax, stepx)))

                ylist = list(map(lambda x: [x[0], make_ylist(x[1])], xlist))

                plot_func()

            elif self.range_input.text() != '' and self.step_input.text() == '':
                xmin = self.range_input.text().split()[0]
                xmax = self.range_input.text().split()[1]
                stepx = ''
                xlist = list(enumerate(make_xlist(xmin, xmax, stepx)))

                ylist = list(map(lambda x: [x[0], make_ylist(x[1])], xlist))

                plot_func()
            elif self.range_input.text() != '' and self.step_input.text() != '':
                xmin = self.range_input.text().split()[0]
                xmax = self.range_input.text().split()[1]
                stepx = self.step_input.text()
                xlist = list(enumerate(make_xlist(xmin, xmax, stepx)))

                ylist = list(map(lambda x: [x[0], make_ylist(x[1])], xlist))

                plot_func()

            self.statusbar.showMessage('')
        except Exception:
            self.statusbar.showMessage('���ОШИБКА ВВОДА���')


# класс окна с инструкцией
class InfoWindow(QWidget, Ui_Form):
    # инструктор
    def __init__(self):
        super(InfoWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Инструкция')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InputWindow()
    ex.show()

    sys.exit(app.exec_())
