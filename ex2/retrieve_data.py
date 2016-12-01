import numpy as np
import pandas as pd
from joblib import Parallel, delayed


class RESOURCE:
    PRESSURE = 'Pf'
    TEMPERATURE = 'TCf'

# create a 2D dataframe for each height level
def to_clean_dataframe(matrix, i):
    print(i)
    df = pd.DataFrame(matrix).apply(lambda row: row.apply(lambda x: np.nan if x >= pow(10, 35) else x))
    return i, df

class DataLoader:

    def __init__(self, resource):
        self.resource = resource
        self.base_path = 'ex2/data/'

    def _get_file_path(self, number):
        if int(number) < 10:
            number = '0{}'.format(int(number))
        return '{}{}{}.bin'.format(self.base_path, self.resource, number)

    def get_data(self, number):
        """
        constructs pd.Panel with a pd.DataFrame for each height level (100)
        :param number: int 1 <= number <= 48
        :return: pd.Panel
        """
        path_file = self._get_file_path(number)
        data = np.fromfile(path_file, dtype='>f')
        tensor = np.reshape(data, (100, 500, 500))
        list_tuples = Parallel(n_jobs=4)(delayed(to_clean_dataframe)(tensor[i], i) for i in range(len(tensor)))
        panel = pd.Panel(dict(list_tuples))
        return panel


def f(x,i):
    return i, pd.DataFrame({'test': [x*2]})

if __name__ == '__main__':
    loader = DataLoader(RESOURCE.TEMPERATURE)
    panel = loader.get_data(1)

