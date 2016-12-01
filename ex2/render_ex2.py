import pandas as pd
import cufflinks
import plotly.plotly as ply
from plotly.graph_objs import *
import plotly.graph_objs as go
import plotly
from ipywidgets import widgets, interact
import os
import sys

from ex2.task1 import Task1

plotly.offline.init_notebook_mode()



@interact(height=widgets.IntSlider(
    value=0,
    min=0,
    max=99,
    step=1,
    description='Altitude z:',
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='i',
    slider_color='white'
    ), __manual=True)
def render_ex2(height):
    task1 = Task1()
    time = 0
    task1.render(time, height)