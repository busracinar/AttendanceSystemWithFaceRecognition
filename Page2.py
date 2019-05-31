from gui import Ui_MainWindow

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

import sqlite3



class Page2(QMainWindow, Ui_MainWindow) :
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        self.setupUi(self)
        self.Load_Database()
        self.Init_Ui()

    def Init_Ui(self):
        self.show()

    def Load_Database(self):

        con = sqlite3.connect('attendance.db')
        cursor = con.cursor()

        content = 'SELECT * FROM attendance'
        result = cursor.execute(content)
        for row_index , row_data in enumerate(result) :
            self.tableWidget.insertRow(row_index)
            for colm_index , colm_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, colm_index, QTableWidgetItem(str(colm_data)))
        con.close()
        return



app = QApplication([])
win = Page2()
app.exec_()