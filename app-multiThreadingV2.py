# 'calculate' function is an inside-class thread and main thread use calculated self.y array
import numpy as np
import pyqtgraph as pg
import threading
import os

class FuncThread(threading.Thread):
    def __init__(self,t,*a):
        self._t=t
        self._a=a
        threading.Thread.__init__(self)
        pid = os.getpid()
        print("In thread , Process is : ",pid)
    def run(self):
        self._t(*self._a)

class MyApp():
    def __init__(self):
        self.number_of_data_steps = 100000
        self.qapp = pg.mkQApp()
        self.win = pg.GraphicsWindow()
        plot1 = self.win.addPlot()
        curve = plot1.plot()
        curve.setPen('r')       
        x = np.linspace(0, self.number_of_data_steps, self.number_of_data_steps)
        self.y = np.linspace(-5, 5, self.number_of_data_steps)
       
        calculating_thread = FuncThread(self.calculate)
        calculating_thread.start()  
        pid = os.getpid()
        print("In main thread , Process is : ",pid)         

        while self.win.isVisible():  
            curve.setData(x,self.y)
            self.qapp.processEvents()

    def calculate(self):
        while self.win.isVisible():  
            self.y += np.random.random(self.number_of_data_steps) - 0.5
                   
if __name__=='__main__': 
    m = MyApp()