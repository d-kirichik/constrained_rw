# -*- coding: utf-8 -*-
from ConstrainedRandomWalk import ConstrainedRandomWalk
import numpy as np
import pandas as pd

df = pd.read_csv('final_MSFT.csv')
df.head()

ts = df['ask_price'].to_numpy()

detrended = np.full(ts.shape[0], 0, dtype=np.float)
for i in range(1, len(ts)):
      detrended[i] = ts[i] - ts[i-1]

crw = ConstrainedRandomWalk(ts, 16, 7)
xs = crw.regenerate_time_series(4000)

np.savetxt('result.csv', xs)
