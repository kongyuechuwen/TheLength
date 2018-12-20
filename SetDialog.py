
from setdialogh_ui import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets



class MyDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_Dialog.__init__(self)
        self.setupUi(self)



    def set_args(self):
        folder_path= self.lineEdit.text()
        log_path = folder_path+"\\img_log\\"