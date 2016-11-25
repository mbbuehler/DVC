import numpy as np



data = range(48)
a = np.array(data)
s = np.reshape(a, (2,4,6))
print(s[:,:,0])
