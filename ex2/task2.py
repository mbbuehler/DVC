
import plotly.graph_objs as go
import plotly
from ex2.retrieve_data import DataLoader, RESOURCE

class Task2:
    def __init__(self):
        self.loader = DataLoader(RESOURCE.PRESSURE)
        self.data = {i: -1 for i in range(1, 49)}

    def _get_data(self, time):
        if self.data[time] != -1:
            return self.data[time]
        else:
            self.data[time] = self.loader.get_data(time)
            return self.data[time]

    def _get_df(self, time, height):
        data = self._get_data(time)
        df = data[height]
        return df

    def render(self, time, height):

        df = self._get_df(time, height)
        trace = go.Contour(
            z=df.values,
            colorbar=go.ColorBar(
                title='Pascals'
                ),
            )
        data = [trace]

        layout = go.Layout(
            title='Pressure for t={} and Altitude (z={}): {:.1f} km'.format(str(time).lstrip('0'), height, height*0.2),
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
    task2 = Task2()
    task2.render(1, 1)