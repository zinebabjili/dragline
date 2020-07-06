from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QThread
import datetime


class Controller(QThread, object):
    now = datetime.datetime.now()
    timeInterval = "%0.2d:%0.2d:%0.2d" % (now.hour, now.minute, now.second)

    newTime = pyqtSignal(object)

    def __init__(self, event):
        QThread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(1):
            self.inTime1()

    def inTime1(self):
        global timeInterval
        now = datetime.datetime.now()
        timeInterval = "%0.2d:%0.2d:%0.2d" % (now.hour, now.minute, now.second)

        self.newTime.emit(timeInterval)
