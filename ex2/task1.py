import plotly.graph_objs as go
import plotly
import sys
from ex2.retrieve_data import DataLoader, RESOURCE

class Task1:
    def __init__(self):
        self.loader = DataLoader(RESOURCE.TEMPERATURE)
        self.data = {i: -1 for i in range(1, 49)}

    def _get_data(self, time):
        if self.data[time] != -1:
            return self.data[time]
        else:
            sys.stdout.write('Loading...')
            self.data[time] = self.loader.get_data(time)
            print(' Done')
            return self.data[time]

    def _get_df(self, time, height):
        data = self._get_data(time)
        df = data[height]
        return df

    def render(self, time, height):

        df = self._get_df(time, height)
        trace = go.Contour(
            z=df.loc[:500, :500].values,
            colorbar=ColorBar(
                title='Temperature'
                ),
            )
        data = [trace]

        layout = go.Layout(
            title='Temperatur for t=01 and Altitude (z={}): {:.1f} km'.format(height, height*0.2),
            xaxis = dict(
                title='Longitude'
            ),
            yaxis = dict(
                title='Latitude'
            ),
        )

        fig = go.Figure(data=data, layout=layout)
        plotly.offline.iplot(fig)

if __name__ == '__main__':
    task1 = Task1()
    task1.render(1, 1)