import numpy as np
#import pyunicorn.eventseries import eca

import ECA

def rand_bin_array(K, N):
    arr = np.zeros(N)
    arr[:K]  = 1
    np.random.shuffle(arr)
    return arr

x = rand_bin_array(5,15)
y = rand_bin_array(5,15)


v = ECA.ECA(x, y, 3, tau=3, ts1=None, ts2=None)

print(x)
print(y) 
print(v)

#pyunicorn.eventseries.eca.ECA(EventSeriesX, EventSeriesY, delT, tau=0, ts1=None, ts2=None)
