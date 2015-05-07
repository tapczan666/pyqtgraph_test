__author__ = 'maciek'
import pyqtgraph

from pyqtgraph.Qt import QtGui, QtCore
from generator import Generator
import numpy as np
import pyqtgraph as pg

app = QtGui.QApplication([])

class Analyzer(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi()
        self.gen = Generator()

        self.generatorThread = QtCore.QThread(self)
        self.gen.moveToThread(self.generatorThread)
        self.generatorThread.started.connect(self.gen.work)

        self.gen.dataUpdated.connect(self.update_plot)

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
        self.waterfall = pg.PlotWidget()
        self.plotLayout.addWidget(self.waterfall)

    def update_plot(self,data):
        self.curve.setData(data)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    analyzer = Analyzer()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
