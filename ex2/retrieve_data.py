import struct

import numpy as np
import pandas as pd


def get_data(path_file, path_out):
    file = open(path_file, 'rb')
    data = []

    bytes = file.read(4)
    i = 0
    # read all bytes from file and add them to a float list (data)
    while bytes != b"":
        i += 1
        if i%1000000 == 0:
            print(i)
        try:
            float = struct.unpack('>f', bytes)[0] # '>f' read as big-endian an float
            data.append(float)
            bytes = file.read(4)
        except:
            bytes = ""

    print('--')
    print(len(data))
    # create a 3D tensor from the 1D array data
    data = np.array(data, dtype=np.dtype(np.float32))
    tensor = np.reshape(data, (100, 500, 500))

    # create a 2D dataframe for each height level
    p = {}
    for i in range(len(tensor)):
        df = pd.DataFrame(tensor[i])
        # clean df. values over 10^30 are invalid
        df = df.apply(lambda row: row.apply(lambda x: np.nan if x > pow(10,30) else x))

        p[i] = df

    # save dataframes in a pd.Panel
    panel = pd.Panel(p)
    panel.to_pickle(path_out)

    file.close()


path_file = 'ex2/data/TCf01.bin'
path_out = 'ex2/data/TCf01.pickle'
# get_data(path_file)$

a = np.array([1,2,3,4,5,6,7,8,9])
s = np.reshape(a, (3,3))
get_data(path_file, path_out)
