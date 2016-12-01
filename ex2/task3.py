import pandas as pd
import plotly.graph_objs as go
import plotly
from ex2.retrieve_data import RESOURCE, TimeSeriesLoader


class Task3:
    def __init__(self):
        self.loader = TimeSeriesLoader()

    def _get_df(self, x, y, z):
        tcf = self.loader.get_data(RESOURCE.TEMPERATURE, x, y, z)
        pf = self.loader.get_data(RESOURCE.PRESSURE, x, y, z)
        index = range(1, 49)
        df = pd.DataFrame({'TCf': tcf,
                           'Pf': pf},
                          index=index)
        return df

    def render(self, x, y, z):
        df = self._get_df(x, y, z)
        trace_tcf = go.Scatter(
            x=list(df.index),
            y=df['TCf'].values,
            name='Temperature'
            )

        trace_pf = go.Scatter(
            x=list(df.index),
            y=df['Pf'].values,
            name='Pressure'
            )

        fig = plotly.tools.make_subplots(rows=2,
                                         cols=1,
                                         subplot_titles=('Temperature', 'Pressure'),
                                         print_grid=False) # dont print grid structure message
        fig.append_trace(trace_tcf, 1, 1)
        fig.append_trace(trace_pf, 2, 1)
        fig['layout'].update(
            title='TimeSeries for Height {:.1f} km (Point x: {}, y: {})'.format(z*0.2, x, y),
        )
        fig['layout']['xaxis1'].update(title='Time (1-48)')
        fig['layout']['xaxis2'].update(title='Time (1-48)')
        fig['layout']['yaxis1'].update(title='Degree Celsius')
        fig['layout']['yaxis2'].update(title='Pascals')

        plotly.offline.iplot(fig, filename='exports/task3')

if __name__ == '__main__':
    task3 = Task3()
    task3._get_df(100, 100, 50)