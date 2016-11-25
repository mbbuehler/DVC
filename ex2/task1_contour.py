import pandas as pd
import plotly
from plotly.graph_objs import *
plotly.offline.init_notebook_mode()

path_dump = 'data/TCf01.pickle'

def get_tcf(z):
    """

    :param z: chosen z value
    :return:
    """
    panel = pd.read_pickle(path_dump)
    df = panel[z]
    return df

df = get_tcf(98)
data = Data([
    Contour(
        z=df.values
    )
])
plotly.offline.iplot(data)
df.loc[:100,:100].plot()