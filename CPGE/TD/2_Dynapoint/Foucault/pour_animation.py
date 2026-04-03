# -*- coding: utf-8 -*-
"""
Created on Wen Dec 31 16:12:01 2021

@author: JM Biansan
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.widgets

class Animateur(FuncAnimation):
    def __init__(self, fig, func, frames=None, init_func=None, fargs=None,
                 save_count=None, datemini=0, datemaxi=100, nombredates=100, pos=(0.125, 0.92), **kwargs):
        self.i = 0
        self.min=0
        self.max=nombredates-1
        self.datemin=datemini
        self.datemax=datemaxi
        self.date=self.datemin
        self.runs = True
        self.forwards = True
        self.fig = fig
        self.func = func
        self.setup(pos)
        FuncAnimation.__init__(self,self.fig, self.func, frames=self.play(),
                                           init_func=init_func, fargs=fargs,
                                           save_count=save_count, **kwargs )

    def play(self):
        while self.runs:
            self.i = self.i+self.forwards-(not self.forwards)
            if self.i > self.min and self.i < self.max:
                yield self.i
            else:
                self.stop()
                yield self.i

    def start(self):
        self.runs=True
        self.event_source.start()

    def stop(self, event=None):
        self.runs = False
        self.event_source.stop()

    def forward(self, event=None):
        self.forwards = True
        self.start()
    def backward(self, event=None):
        self.forwards = False
        self.start()
    def oneforward(self, event=None):
        self.runs = False
        self.event_source.stop()
        self.forwards = True
        self.onestep()
    def onebackward(self, event=None):
        self.runs = False
        self.event_source.stop()
        self.forwards = False
        self.onestep()
    def onestep(self):
        if self.i > self.min and self.i < self.max:
            self.i = self.i+self.forwards-(not self.forwards)
        elif self.i == self.min and self.forwards:
            self.i+=1
        elif self.i == self.max and not self.forwards:
            self.i-=1
        self.func(self.i)
        self.fig.canvas.draw_idle()
    def update_date(self,val):
        self.i=int((self.date_slider.val-self.datemin)/(self.datemax-self.datemin)*self.max)
        self.func(self.i)
        self.fig.canvas.draw_idle()

    def setup(self, pos):

        w_one_back=plt.axes([0, 0.95, 0.05, 0.05])
        w_back=plt.axes([0.05, 0.95, 0.05,  0.05])
        w_stop=plt.axes([0.1, 0.95, 0.05,  0.05])
        w_forward=plt.axes([0.15, 0.95, 0.05,  0.05])
        w_one_forward=plt.axes([0.20, 0.95, 0.05,  0.05])
        w_slide=plt.axes([0.35, 0.95, 0.6, 0.05])

        self.button_oneback = matplotlib.widgets.Button(w_one_back,label='-1')
        self.button_back = matplotlib.widgets.Button(w_back, label='<-')
        self.button_stop = matplotlib.widgets.Button(w_stop, label='=')
        self.button_forward = matplotlib.widgets.Button(w_forward, label='->')
        self.button_oneforward = matplotlib.widgets.Button(w_one_forward, label='+1')
        self.button_oneback.on_clicked(self.onebackward)
        self.button_back.on_clicked(self.backward)
        self.button_stop.on_clicked(self.stop)
        self.button_forward.on_clicked(self.forward)
        self.button_oneforward.on_clicked(self.oneforward)
        self.date_slider = matplotlib.widgets.Slider(ax=w_slide,label='Date',valmin=self.datemin,valmax=self.datemax,valinit=self.datemin,)
        self.date_slider.on_changed(self.update_date)


