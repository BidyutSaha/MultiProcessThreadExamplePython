import random
import os
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import multiprocessing as mp
import time
#from pyqtgraph.dockarea import *

class PLT():
    def __init__(self):
        self.win = pg.GraphicsWindow(title="Basic plotting examples")
        self.win.setWindowTitle('pyqtgraph example: Plotting')
        #self.win.resize(1000,600)
        self.p2 = self.win.addPlot(title="Updating plot")
        self.curve = self.p2.plot(pen='y')

        #QtGui.QApplication.instance().exec_()   # ---> if it's in effect, the plotting window shows up, but the data exchange doesn't happen.

    def update(self, data):
        self.curve.setData(data)
        QtGui.QApplication.processEvents()   # <--- Here is the way to update the window.

class sender(mp.Process):
    def __init__(self, pipe):
        mp.Process.__init__(self)
        self.pipe = pipe

    def run(self):
        pid = os.getpid()
        print('SENDER PID: ', pid )

        while True:
            value = random.randint(0, 10)
            self.pipe.send(value)
            print("Sender is running!",pid)
            time.sleep(.01)

class receiver(mp.Process):
    def __init__(self, pipe):
        mp.Process.__init__(self)
        self.pipe = pipe

    def run(self):
        self.p = PLT()
        pid = os.getpid()
        print('RECEIVER PID: ', pid )
        while True:
            integer = self.pipe.recv() 
            print("Reciver is running!",pid, integer)  

            self.p.update(np.random.normal(size=(10,1000))[integer%10])

if __name__ == '__main__':
    mp.freeze_support()
    print('MAIN PID: ', os.getpid() )

    out_pipe, in_pipe = mp.Pipe() 

    p1 = sender(pipe=in_pipe)
    p2 = receiver(pipe=out_pipe)
    p1.start()
    p2.start()