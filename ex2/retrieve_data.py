import abc

import numpy as np
import pandas as pd
import sys
from joblib import Parallel, delayed


class RESOURCE:
    PRESSURE = 'Pf'
    TEMPERATURE = 'TCf'


# create a 2D dataframe for each height level
def to_clean_dataframe(matrix, i):
    df = pd.DataFrame(matrix).apply(lambda row: row.apply(lambda x: np.nan if x >= pow(10, 35) else x))
    return i, df



class AbstractLoader():
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.base_path = 'data/'

    def _get_file_path(self, resource, number):
        if int(number) < 10:
            number = '0{}'.format(int(number))
        return '{}{}{}.bin'.format(self.base_path, resource, number)

    @staticmethod
    def get_file_data_array(path_file):
        return np.fromfile(path_file, dtype='>f')

    def get_value(self, resource, time, x, y, z):
        path_file = self._get_file_path(resource, time)
        data = self.get_file_data_array(path_file)
        index = self.get_index(x, y, z)
        return data[index]

    @staticmethod
    def get_index(x, y, z):
        return x+500 * (y + 500 * z)


class DataLoader(AbstractLoader):
    def __init__(self, resource):
        super(DataLoader, self).__init__()
        self.resource = resource

    def get_data(self, number):
        """
        constructs pd.Panel with a pd.DataFrame for each height level (100)
        :param number: int 1 <= number <= 48
        :return: dict
        """
        path_file = self._get_file_path(self.resource, number)
        data = self.get_file_data_array(path_file)
        tensor = np.reshape(data, (100, 500, 500))
        list_tuples = Parallel(n_jobs=4)(delayed(to_clean_dataframe)(tensor[i], i) for i in range(len(tensor)))
        data = dict(list_tuples)
        return data


class TimeSeriesLoader(AbstractLoader):
    def __init__(self):
        super(TimeSeriesLoader, self).__init__()
        self.time_min = 1
        self.time_max = 48

    def get_data(self, resource, x, y, z):
        """
        :param resource: RESOURCE
        :param x: index for longitude 0<=x<=499
        :param y: index for latitude 0<=x<=499
        :param z: index for z 0<=z<=99
        :return:
        """
        data = Parallel(n_jobs=4)(delayed(self.get_value)(resource, time, x, y, z) for time in range(self.time_min, self.time_max+1))
        return data


if __name__ == '__main__':
    # loader = DataLoader(RESOURCE.TEMPERATURE)
    # panel = loader.get_data(1)

    loader = TimeSeriesLoader()
    loader.get_data(RESOURCE.TEMPERATURE, 200, 200, 5)

