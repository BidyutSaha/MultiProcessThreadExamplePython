import random
import os
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import multiprocessing as mp
import time
import threading
#from pyqtgraph.dockarea import *

class PLT():
    def __init__(self):
        self.win = pg.GraphicsWindow(title="Basic plotting examples")
        self.win.setWindowTitle('pyqtgraph example: Plotting')
        self.p2 = self.win.addPlot(title="Updating plot")
        self.curve = self.p2.plot(pen='y')

    def update(self, data):
        self.curve.setData(data)
        QtGui.QApplication.processEvents()   # <--- Here is the way to update the window.


class receiver():
    def __init__(self):
        self.p = PLT()
        self.data  = 5


    def threaded_method(self):
        while True:
            self.data=np.random.randint(5,100)
            time.sleep(.01)
        

    def run(self):
        
        pid = os.getpid()
        print('RECEIVER PID: ', pid )

        threading.Thread(target=self.threaded_method).start()
        while True:
            print(self.data)
            self.p.update(np.random.normal(size=(10,1000))[self.data%10])

if __name__ == '__main__':
    mp.freeze_support()
    print('MAIN PID: ', os.getpid() )
    p = receiver()
    p.run()