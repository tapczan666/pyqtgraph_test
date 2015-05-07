__author__ = 'maciek'
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import time

class Generator(QtCore.QObject):

    dataUpdated = QtCore.pyqtSignal(object)
    def __init__(self, parent=None):
        super(Generator, self).__init__(parent)
        self.data = np.random.normal(size=(10,1000))
        self.ptr = 0

    def work(self):
        while True:
            temp = self.data[self.ptr%10]
            self.dataUpdated.emit(temp)
            if self.ptr==9:
                self.ptr = 0
            else:
                self.ptr += 1
            time.sleep(0.1)

