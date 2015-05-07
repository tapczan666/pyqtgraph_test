__author__ = 'maciek'
import pyqtgraph

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
#from generator import Generator
import numpy as np
import pyqtgraph as pg
import time

app = QtGui.QApplication([])

class Analyzer(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.waterfallHistorySize = 100
        self.setupUi()
        self.gen = Generator()

        self.generatorThread = QtCore.QThread(self)
        self.gen.moveToThread(self.generatorThread)
        self.generatorThread.started.connect(self.gen.work)

        self.gen.dataUpdated.connect(self.updatePlot)
        self.gen.dataUpdated.connect(self.updateWaterfall)

        self.generatorThread.start()

    def setupUi(self):
        self.mw = QtGui.QWidget()
        self.mw.setWindowTitle('Analyzer')
        self.plotLayout = QtGui.QVBoxLayout()
        self.mw.setLayout(self.plotLayout)

        #Adding main plot
        self.createPlot()
        #Adding waterfall plot
        self.createWaterfall()

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)
        self.mw.show()

    def createPlot(self):
        self.plot = pg.PlotWidget()
        self.plotLayout.addWidget(self.plot)
        self.plot.showGrid(x=True, y=True)
        self.plot.setYRange(-4, 4)
        self.curve = self.plot.plot(pen='y')

    def createWaterfall(self):
        self.waterfallPlot = pg.PlotWidget()
        self.plotLayout.addWidget(self.waterfallPlot)
        self.waterfallPlot.setYRange(-self.waterfallHistorySize, 0)
        self.waterfallPlot.setXLink(self.plot)

        self.waterfallImg = None

    @pyqtSlot(object)
    def updatePlot(self,data):
        self.curve.setData(data)

    @pyqtSlot(object)
    def updateWaterfall(self, data):
        if self.waterfallImg is None:
            self.waterfallImgArray = np.zeros((self.waterfallHistorySize, len(data)))
            self.waterfallImg = pg.ImageItem()
            self.waterfallImg.scale((data[-1] - data[0]) / len(data), 1)
            self.waterfallPlot.clear()
            self.waterfallPlot.addItem(self.waterfallImg)

        self.waterfallImgArray = np.roll(self.waterfallImgArray, -1, axis=0)
        self.waterfallImgArray[-1] = data
        self.waterfallImg.setImage(self.waterfallImgArray.T,
                                   autoLevels=True, autoRange=True)


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

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    analyzer = Analyzer()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
