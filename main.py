#!/usr/bin/env python3

import parser_controller
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QTextBrowser,
    QVBoxLayout,
    QWidget
)
from PyQt5.QtGui import QIcon
from requests import exceptions as req_ex
import sys
import os

icon_path = r'icons8-book-64.png'


class Project_X(QMainWindow):
    search_line = None
    search_btn = None
    res_text = None
    filename = None
    permanentStatusLbl = None
    statusbar = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Project-x')
        self.setGeometry(300, 300, 720, 480)
        self.setWindowIcon(QIcon(icon_path))
        self.initUI()

    def initUI(self):
        self._createMenu()
        self._createStatusBar()
        self._addWidgetsToLayout()

    def _createMenu(self):
        menuBar = self.menuBar()
        
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)

        openAction = QAction("&Open", self)
        saveAction = QAction("&Save", self)
        openAction.triggered.connect(self.openfile)
        saveAction.triggered.connect(self.savefile)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)

        aboutMenu = QMenu("&About", self)
        menuBar.addMenu(aboutMenu)
        aboutAction = QAction("&about", self)
        aboutMenu.addAction(aboutAction)

    def _createStatusBar(self):
        self.statusbar = QStatusBar()
        self.statusbar.showMessage("Status Bar")
        self.setStatusBar(self.statusbar)
        self.permanentStatusLbl = QLabel(f"{self.permanentStatus()}")
        self.statusbar.addPermanentWidget(self.permanentStatusLbl)

    def _addWidgetsToLayout(self):
        centralWidget = QWidget()
        mainLayout = QVBoxLayout()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        search_box = QWidget()
        search_box_l = QHBoxLayout()
        search_box.setLayout(search_box_l)

        self.search_line = QLineEdit()
        search_box_l.addWidget(self.search_line)
        self.search_line.returnPressed.connect(self.search_btn_clicked)

        self.search_btn = QPushButton("Search")
        search_box_l.addWidget(self.search_btn)
        self.search_btn.clicked.connect(self.search_btn_clicked)

        mainLayout.addWidget(search_box)

        self.res_text = QTextBrowser()
        self.res_text.setReadOnly(True)
        mainLayout.addWidget(self.res_text)

    def permanentStatus(self):
        return "permanent status"

    def openfile(self):
        cwd = os.getcwd()
        fname = QFileDialog.getOpenFileName(self, 'Open file', cwd, "Text files (*.txt)")[0]
        file_content = ''
        with open(fname, 'r') as f:
            file_content = f.read()
        self.res_text.setText(file_content)
        self.statusbar.showMessage(f"open file: {fname}")

    def savefile(self):
        cwd = os.getcwd()
        savefile_name = QFileDialog.getSaveFileName(self, 'Save file', cwd, "Text files (*.txt)")[0]
        with open(savefile_name, 'w+') as f:
            f.write(self.res_text.toPlainText())
        self.statusbar.showMessage(f"save file: {savefile_name}")

    def show_msgBox(self, severityLvl=QMessageBox.Warning, text="no info"):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Error occurred")
        msgBox.setIcon(severityLvl)
        msgBox.setText(text)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    def search_btn_clicked(self):
        self.res_text.clear()
        search_string = self.search_line.text()

        try:
            for parser in parser_controller.project_x_parsers:
                res = parser(search_string)
                self.res_text.append('site: ' + res['domain'] + '\n')
                for i, idiom in enumerate(res['idioms']):
                    self.res_text.append(str(i) + '. ' + idiom['title'] + '\n')
                    self.res_text.append(str(idiom['description']) + '\n')
                    self.res_text.append(idiom['example'] + '\n')
                    self.res_text.append('--------------' + '\n')
        except req_ex as e:
            self.show_msgBox(severityLvl=QMessageBox.Warning, text=e)
        except BaseException as b:
            self.show_msgBox(severityLvl=QMessageBox.Warning, text=b)


def main():
    app = QApplication(sys.argv)
    ui = Project_X()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
