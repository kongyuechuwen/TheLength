from PyQt5.QtCore import *
import GlobalData
import time
import watch_directory
import os,sys,queue
import Distance

class WorkThread(QThread):

    finished = pyqtSignal()
    intReady = pyqtSignal(str)


    def scan(self):

               # while True:
        #     time.sleep(1)
        #     self.intReady.emit("#:  "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +"   系统检测。。。")

        PATH_TO_WATCH = [GlobalData.FILE_PATH]
        path_to_watch = PATH_TO_WATCH
        # PATH_TO_WATCH = "."
        # try:
        #     path_to_watch = sys.argv[1].split(",") or PATH_TO_WATCH
        # except:
        #     path_to_watch= PATH_TO_WATCH
        #
        # print(path_to_watch)
        # path_to_watch = [os.path.abspath(p) for p in path_to_watch]
        # print(path_to_watch)
        # print([GlobalData.FILE_PATH])

        # for p in path_to_watch:
        #     print(p)
        #
        # path_to_watch=[path_to_watch]
        # print(path_to_watch)


        self.intReady.emit("#: %s   开始监测： %s" % ( time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,path_to_watch))

        files_changed = queue.Queue()

        for p in path_to_watch:
            watch_directory.Watcher(p, files_changed)
 
        while 1:
            if GlobalData.SCAN_FLAG:
                try:
                    file_type, filename, action = files_changed.get_nowait()

                    if(str(file_type)=="file" and action=="Created" and str(filename)[-3:] == "jpg"):
                        f = open(str(filename).replace(".", "-") + "-result.log", 'w')

                        try:
                            cimg, circles, min, max = Distance.measure_distance(filename)
                            print(filename)

                            f_name = os.path.basename(filename)
                            ip_time = f_name.split("_")

                            f.write(ip_time[0]+'  ' + ip_time[2][0:4]+'-'+ip_time[2][4:6]+
                                     '-'+ip_time[2][6:8]+' '+ip_time[2][8:10]+':'
                                     +ip_time[2][10:12]+':'+ip_time[2][12:14]+':'
                                     +ip_time[2][14:17] )
                           

                            if (circles[0, 0, 0] > max or circles[0, 0, 0] < min):

                                l1 = abs(float(circles[0, 1, 0] - float(circles[0, 0, 0])))
                                l2 = abs(float(circles[0, 2, 0] - float(circles[0, 0, 0])))
                                if (l1 < l2):
                                    f.write("  " + str(l1*0.25) + "mm")
                                else:
                                    f.write("  " + str(l2*0.25) + "mm")

                            if (circles[0, 1, 0] > max or circles[0, 1, 0] < min):

                                l1 = abs(float(circles[0, 0, 0] - float(circles[0, 1, 0])))
                                l2 = abs(float(circles[0, 2, 0] - float(circles[0, 1, 0])))
                                if (l1 < l2):
                                    f.write("  " + str(l1*0.25) + "mm")
                                else:
                                    f.write("  " + str(l2*0.25) + "mm")

                            if (circles[0, 2, 0] > max or circles[0, 2, 0] < min):

                                l1 = abs(float(circles[0, 0, 0] - float(circles[0, 2, 0])))
                                l2 = abs(float(circles[0, 1, 0] - float(circles[0, 2, 0])))
                                if (l1 < l2):
                                    f.write("  " + str(l1*0.25) + "mm")
                                else:
                                    f.write("  " + str(l2*0.25) + "mm")

                            f.close()
                        except Exception as e:
                            f.close()

                            f_err = open(str(filename).replace(".", "-")+"-err.log", 'w')
                            f_err.write(e)
                            f_err.close()

                    self.intReady.emit("#:  " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +"   "+
                                       file_type+" | "+filename+"  | " + action)
                except queue.Empty:
                    pass
                time.sleep(1)
            else:
                break

        self.intReady.emit(
            "#: %s  停止监测： %s \n\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), path_to_watch))
        self.finished.emit()

