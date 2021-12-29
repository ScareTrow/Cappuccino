import sys
import sqlite3

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        global self_programm
        self_programm = self
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.db")
        self.write_to_table()
        self.createEntry.clicked.connect(self.create_entry)
        self.refreshButton.clicked.connect(self.write_to_table)

    def create_entry(self):
        self.form = Window()
        self.form.show()

    def write_to_table(self):
        cur = self.con.cursor()
        result = cur.execute(f"""SELECT * FROM information
                             ORDER BY ID""").fetchall()

        self.tableWidget.setRowCount(len(result))

        if not result:
            return
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

        header = self.tableWidget.horizontalHeader()
        title = ["ID", "sorts_name", "degree_of_roast", "ground_or_grains",
                 "flavor_description", "price", "packing_volume"]

        self.tableWidget.setHorizontalHeaderLabels(title)
        self.result = list()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        for i in range(1, len(title)):
            header.setSectionResizeMode(
                i, QtWidgets.QHeaderView.ResizeToContents)


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.update_button.clicked.connect(self.update)
        self.add_entry_button.clicked.connect(self.add)

    def update(self):
        ID = self.ID_input.text()
        sorts_name = self.sort_type.text()
        degree_of_roast = self.roast_text.text()
        consistency = self.consistency_text.text()
        description = self.description_text.text()
        price = self.price_text.text()
        volume = self.volume_text.text()

        con = sqlite3.connect("coffee.db")
        cur = con.cursor()

        if sorts_name != "":
            cur.execute(f'''UPDATE information SET sorts_name = "{sorts_name}"
                            WHERE ID = "{ID}"''')
        if degree_of_roast != "":
            cur.execute(f'''UPDATE information SET degree_of_roast = "{degree_of_roast}"
                            WHERE ID = "{ID}"''')
        if consistency != "":
            cur.execute(f'''UPDATE information SET ground_or_grains = "{consistency}"
                            WHERE ID = "{ID}"''')
        if description != "":
            cur.execute(f'''UPDATE information SET flavor_description = "{description}"
                            WHERE ID = "{ID}"''')
        if price != "":
            cur.execute(f'''UPDATE information SET price = "{price}"
                            WHERE ID = "{ID}"''')
        if volume != "":
            cur.execute(f'''UPDATE information SET packing_volume = "{volume}"
                            WHERE ID = "{ID}"''')
        con.commit()
        self_programm.form.close()
        self_programm.write_to_table()

    def add(self):
        ID = self.ID_input.text()
        sorts_name = self.sort_type.text()
        degree_of_roast = self.roast_text.text()
        consistency = self.consistency_text.text()
        description = self.description_text.text()
        price = self.price_text.text()
        volume = self.volume_text.text()

        con = sqlite3.connect("coffee.db")
        cur = con.cursor()
        cur.execute(f"INSERT OR IGNORE INTO information VALUES ('{ID}', '{sorts_name}', '{degree_of_roast}',"
                    f" '{consistency}', '{description}', '{price}', '{volume}')")
        con.commit()
        self_programm.form.close()
        self_programm.write_to_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
