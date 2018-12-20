# -*- coding:utf-8-*-

import sys
import threading

import time

import Distance
from main_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

import cv2
import os
import numpy as np
import watch_directory
import matplotlib.pyplot as plt
from Distance import measure_distance
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import random
import ScanThread
from setdialogh_ui import Ui_Dialog
import GlobalData

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

folder_path = "C:\\"

class MyDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_Dialog.__init__(self)
        self.setupUi(self)

        # log_path

        self.pushButton.clicked.connect(self.set_monitor_folder)
        self.pushButton_2.clicked.connect(self.set_log_folder)
        self.buttonBox.accepted.connect(self.accept)


    def set_monitor_folder(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, '选择文件夹')
        self.lineEdit.setText(directory)
        self.lineEdit_2.setText(directory)

    def set_log_folder(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, '选择文件夹')
        self.lineEdit_2.setText(directory)

    def accept(self):

        log_path = self.lineEdit_2.text()
        GlobalData.FILE_PATH = self.lineEdit.text()
        f = open("length.config", "w")
        try:
            f.write("\""+GlobalData.FILE_PATH+"/\"")
        finally:
            f.close()

        print(GlobalData.FILE_PATH)
        self.close()


class ImageWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.flag = True

        app_icon = QtGui.QIcon()
        app_icon.addFile('img/16.ico', QtCore.QSize(16, 16))
        app_icon.addFile('img/24.ico', QtCore.QSize(24, 24))
        app_icon.addFile('img/32.ico', QtCore.QSize(32, 32))
        app_icon.addFile('img/48.ico', QtCore.QSize(48, 48))
        app_icon.addFile('img/64.png', QtCore.QSize(64, 64))
        app_icon.addFile('img/128.ico', QtCore.QSize(128, 128))
        app_icon.addFile('img/256.ico', QtCore.QSize(256, 256))

        self.setWindowIcon(QtGui.QIcon(app_icon))

        # self.textEdit.append(" ==================================")
        # self.textEdit.append(" ||     ZHENG WEN 2016-11-18     ||")
        # self.textEdit.append(" ==================================")
        self.arr = None
        # self.pushButton.clicked.connect(self.buttonClicked)

        # a figure instance to plot on
        self.figure = plt.figure()

        img = cv2.imread("1.jpg", 0)
        img = cv2.medianBlur(img, 5)
        cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # self.canvas = FigureCanvas(cimg)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QtWidgets.QPushButton('分析')

        self.verticalLayout_7.addWidget(self.toolbar)
        self.verticalLayout_7.addWidget(self.canvas)
        self.verticalLayout_7.addWidget(self.button)

        self.path = "1.jpg"

        self.trayIcon = QtWidgets.QSystemTrayIcon(self)
        self.trayIcon.setIcon(app_icon)
        self.trayIcon.show()

        self.menu = QtWidgets.QMenu()
        self.max_action = self.menu.addAction("最大化")
        self.exit_action = self.menu.addAction("退出")
        self.trayIcon.setContextMenu(self.menu)

        self.exit_action.triggered.connect(self.quit)
        self.max_action.triggered.connect(self.max)
        self.button.clicked.connect(self.plot_img)

        self.pushButton.clicked.connect(self.img_path)
        self.pushButton_3.clicked.connect(self.start_scan)
        self.pushButton_4.clicked.connect(self.stop_scan)
        self.pushButton_2.clicked.connect(self.open_folder)
        self.pushButton_5.clicked.connect(self.open_dialog)

        #  去除border
        self.groupBox_9.setStyleSheet("QGroupBox{ border: 0px;}")
        self.groupBox_10.setStyleSheet("QGroupBox{ border: 0px;}")

        self.obj = ScanThread.WorkThread()  # no parent!
        # no parent!
        self.thread = QtCore.QThread()  # no parent!

        # 2 - Connect Worker`s Signals to Form method slots to post data.
        self.obj.intReady.connect(self.start_scan)

        # 3 - Move the Worker object to the Thread object
        self.obj.moveToThread(self.thread)

        # 4 - Connect Worker Signals to the Thread slots
        self.obj.finished.connect(self.thread.quit)

        # 5 - Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.obj.scan)

        # * - Thread finished signal will close the app if you want!
        self.thread.finished.connect(self.thread_stop)

    def closeEvent(self, evnt):
        evnt.ignore()
        self.hide()
        self.setWindowState(QtCore.Qt.WindowMinimized)

    def test(self):
        print("hello world!")

    def quit(self):
        self.quit()

    def max(self):
        # self.show()
        self.showNormal()
        # self.showMaximized()

    def img_path(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Image files (*.jpg *.gif)")
        self.lineEdit.setText(fname[0])
        # self.path = str(fname[0]).encode('utf-8')
        self.path = str(fname[0])

        # print(fname[0])

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()

    def plot_img(self):

        try:
            cimg, circles, min, max = measure_distance(self.path)

            # print(circles, min, max)

            ax = self.figure.add_subplot(111)
            ax.imshow(cimg)
            self.canvas.draw()

            self.lineEdit_2.setText('')
            self.lineEdit_3.setText('')
            self.lineEdit_4.setText('')
            self.lineEdit_5.setText('')
            self.lineEdit_6.setText('')
            self.lineEdit_7.setText('')

            self.lineEdit_14.setText('')
            self.lineEdit_15.setText('')
            self.lineEdit_16.setText('')

            # print(circles)
            # print(circles[0, 0],circles[0, 1],circles[0, 2])
            # print(circles[0, 0,1],circles[0, 1,2],circles[0, 2,2])

            try:
                if (circles[0, 0, 0] > max or circles[0, 0, 0] < min):

                    self.lineEdit_6.setText("(" + str(circles[0, 0, 0]) + "," + str(circles[0, 0, 1]) + ")")
                    self.lineEdit_7.setText("" + str(circles[0, 0, 2]* (1.5 / 60))+ 'cm')
                    # self.lineEdit_3.setText(str(circles[0,0,2]))

                    self.lineEdit_4.setText("(" + str(circles[0, 1, 0]) + "," + str(circles[0, 1, 0]) + ")")
                    self.lineEdit_5.setText("" + str(circles[0, 1, 2] * (1.5 / 60)) + 'cm')
                    # self.lineEdit_5.setText(str(circles[0, 1, 2]))

                    self.lineEdit_2.setText("(" + str(circles[0, 2, 0]) + "," + str(circles[0, 2, 1]) + ")")
                    self.lineEdit_3.setText("" + str(circles[0, 2, 2] * (1.5 / 60)) + 'cm')
                    # self.lineEdit_7.setText(str(circles[0, 2, 2]))

                    l1 = abs(float(circles[0, 1, 0] - float(circles[0, 0, 0])))
                    l2 = abs(float(circles[0, 2, 0] - float(circles[0, 0, 0])))
                    if (l1 < l2):
                        self.lineEdit_14.setText(str(l1* (1.5 / 60)) + 'cm')
                    else:
                        self.lineEdit_14.setText(str(l2* (1.5 / 60)) + 'cm')

                if (circles[0, 1, 0] > max or circles[0, 1, 0] < min):

                    self.lineEdit_2.setText("(" + str(circles[0, 0, 0]) + "," + str(circles[0, 0, 1]) + ")")
                    self.lineEdit_3.setText("" + str(circles[0, 0, 2]* (1.5 / 60)) + 'cm')
                    # self.lineEdit_3.setText(str(circles[0,0,2]))

                    self.lineEdit_6.setText("(" + str(circles[0, 1, 0]) + "," + str(circles[0, 1, 1]) + ")")
                    self.lineEdit_7.setText("" + str(circles[0, 1, 2]* (1.5 / 60)) + 'cm')
                    # self.lineEdit_5.setText(str(circles[0, 1, 2]))

                    self.lineEdit_4.setText("(" + str(circles[0, 2, 0]) + "," + str(circles[0, 2, 1]) + ")")
                    self.lineEdit_5.setText("" + str(circles[0, 2, 2]* (1.5 / 60)) + 'cm')
                    # self.lineEdit_7.setText(str(circles[0, 2, 2]))

                    l1 = abs(float(circles[0, 0, 0] - float(circles[0, 1, 0])))
                    l2 = abs(float(circles[0, 2, 0] - float(circles[0, 1, 0])))
                    if (l1 < l2):
                        self.lineEdit_14.setText(str(l1* (1.5 / 60)) + 'cm')
                    else:
                        self.lineEdit_14.setText(str(l2* (1.5 / 60)) + 'cm')

                if (circles[0, 2, 0] > max or circles[0, 2, 0] < min):

                    self.lineEdit_2.setText("(" + str(circles[0, 0, 0]) + "," + str(circles[0, 0, 1]) + ")")
                    self.lineEdit_3.setText("" + str(circles[0, 0, 2]* (1.5 / 60)) + 'cm')
                    # self.lineEdit_3.setText(str(circles[0,0,2]))

                    self.lineEdit_4.setText("(" + str(circles[0, 1, 0]) + "," + str(circles[0, 1, 1]) + ")")
                    self.lineEdit_5.setText("" + str(circles[0, 1, 2]* (1.5 / 60)) + 'cm')
                    # self.lineEdit_5.setText(str(circles[0, 1, 2]))

                    self.lineEdit_6.setText("(" + str(circles[0, 2, 0]) + "," + str(circles[0, 2, 1]) + ")")
                    self.lineEdit_7.setText("" + str(circles[0, 2, 2]* (1.5 / 60)) + 'cm')
                    # self.lineEdit_7.setText(str(circles[0, 2, 2]))

                    l1 = abs(float(circles[0, 0, 0] - float(circles[0, 2, 0])))
                    l2 = abs(float(circles[0, 1, 0] - float(circles[0, 2, 0])))
                    if (l1 < l2):
                        self.lineEdit_14.setText(str(l1* (1.5 / 60)) + 'cm')
                    else:
                        self.lineEdit_14.setText(str(l2* (1.5 / 60)) + 'cm')

                # a = abs(abs(circles[0, 0, 0] - circles[0, 1, 0])-120)
                # b = abs(abs(circles[0, 1, 0] - circles[0, 2, 0])-120)

                # l1 = abs(float(circles[0, 1, 0]-float(circles[0, 0, 0])))*(1.5/60)
                # l2 = abs(float(circles[0, 2, 0]-float(circles[0, 0, 0])))*(1.5/60)
                # l3 = abs(float(circles[0, 1, 0]-float(circles[0, 2, 0])))*(1.5/60)
                #
                # x1 = l1-120
                # # print(float(circles[0, 0, 0]))
                # if abs(l1-120) < abs(l2-120) and abs(l1-120)<abs(l3-120):
                #     self.lineEdit_14.setText(str(l1) + "像素")
                #
                # if float(circles[0, 0, 0]) <= float(circles[0, 1, 0]):
                #     self.lineEdit_14.setText(str(l1)+"像素")
                # else:
                #     self.lineEdit_14.setText(str(l1)+"像素")

                # if(circles[0, 1, 0] > max)
                #     self.lineEdit_14.setText(str(l1) + "像素")

                # plt.imshow(cimg)
                self.textBrowser_2.setText("success")
            except Exception as err:
                self.textBrowser_2.setText(str(circles))

            # 路径显示
            try:
                fileName = os.path.basename(self.path)
                ip_time = fileName.split("_")

                self.lineEdit_15.setText(ip_time[2][0:4] + '-' + ip_time[2][4:6] +
                                         '-' + ip_time[2][6:8] + ' ' + ip_time[2][8:10] + ':'
                                         + ip_time[2][10:12] + ':' + ip_time[2][12:14] + ':'
                                         + ip_time[2][14:17])
                self.lineEdit_16.setText(ip_time[0])
            except Exception as err:
                self.lineEdit_15.setText("文件名不合规")
                self.textBrowser_2.append("文件名不合规:" + fileName)
        except:
            pass



    def start_scan(self, i):
        # if self.flag:
        #     self.pushButton_4.setText("停止检测")
        # print("lll")
        GlobalData.SCAN_FLAG = True
        self.stackedWidget.setCurrentIndex(1)

        self.textBrowser.append("{}".format(i))

        # self.textBrowser.append(i)
        # self.thread.start()

        filenames = self.file_name(GlobalData.FILE_PATH)
        threading.Thread(target=self.old_img_calc, args=(filenames,)).start()

        #     self.flag = False
        # else:
        #     self.pushButton_4.setText("停止监测")
        #     self.flag = True

    def stop_scan(self):

        GlobalData.SCAN_FLAG = False
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget.show()
        print(self.stackedWidget.currentIndex())

    def thread_stop(self):
        self.stackedWidget.setCurrentIndex(0)
        print("222")


    def open_folder(self):
        global folder_path
        print(folder_path)
        import subprocess
        subprocess.Popen('explorer '+ folder_path)
        # subprocess.Popen('explorer "D://"')

    def open_dialog(self):
        # Dialog = QtWidgets.QDialog()
        self.my_dialog = MyDialog()
        self.my_dialog.show()
        # sys.exit(Dialog.exec_())

    # get filename list
    def file_name(self, file_dir):
        for root, dirs, files in os.walk(file_dir):
            return files

    def old_img_calc(self, filenames):
        # pass
        for i in range(len(filenames)):
            filename = GlobalData.FILE_PATH+"/"+filenames[i]
            try:
                f1 = open(str(filename).replace(".", "-") + "-result.log", 'w')
                cimg1, circles1, min1, max1 = Distance.measure_distance(filename)
                print(filename)

                f_name1 = os.path.basename(filename)
                ip_time1 = f_name1.split("_")

                f1.write(ip_time1[0] + '  ' + ip_time1[2][0:4] + '-' + ip_time1[2][4:6] +
                         '-' + ip_time1[2][6:8] + ' ' + ip_time1[2][8:10] + ':'
                         + ip_time1[2][10:12] + ':' + ip_time1[2][12:14] + ':'
                         + ip_time1[2][14:17])

                if (circles1[0, 0, 0] > max1 or circles1[0, 0, 0] < min1):

                    l11 = abs(float(circles1[0, 1, 0] - float(circles1[0, 0, 0])))
                    l21 = abs(float(circles1[0, 2, 0] - float(circles1[0, 0, 0])))
                    if (l11 < l21):
                        f1.write("  " + str(l11) + "mm")
                    else:
                        f1.write("  " + str(l21) + "mm")

                if (circles1[0, 1, 0] > max1 or circles1[0, 1, 0] < min1):

                    l11 = abs(float(circles1[0, 0, 0] - float(circles1[0, 1, 0])))
                    l21 = abs(float(circles1[0, 2, 0] - float(circles1[0, 1, 0])))
                    if (l11 < l21):
                        f1.write("  " + str(l11) + "mm")
                    else:
                        f1.write("  " + str(l21) + "mm")

                if (circles1[0, 2, 0] > max1 or circles1[0, 2, 0] < min1):

                    l11 = abs(float(circles1[0, 0, 0] - float(circles1[0, 2, 0])))
                    l21 = abs(float(circles1[0, 1, 0] - float(circles1[0, 2, 0])))
                    if (l11 < l21):
                        f1.write("  " + str(l11) + "mm")
                    else:
                        f1.write("  " + str(l21) + "mm")

                f1.close()
                self.textBrowser.append("#:  之前的文件" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "   " + filenames[i] + "已经处理完毕！")
            except Exception as e:
                f1.close()
                f_err = open(str(filename).replace(".", "-") + "-err.log", 'w')
                self.textBrowser.append("#:  之前的文件" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "   " + filenames[i] + "已经处理失败！")
                f_err.write(str(e))
                f_err.close()


def main():
    GlobalData.set_path()

    app = QtWidgets.QApplication(sys.argv)
    win = ImageWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
