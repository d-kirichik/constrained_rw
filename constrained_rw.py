# -*- coding: utf-8 -*-
from ConstrainedRandomWalk import ConstrainedRandomWalk
import numpy as np
import pandas as pd
import sys

input_file = sys.argv[1]
z_vector_size = sys.argv[2]
tau = sys.argv[3]
regenerated_size = sys.argv[4]
output_file = sys.argv[5]

df = pd.read_csv(input_file)
df.head()

ts = df['ask_price'].to_numpy()

detrended = np.full(ts.shape[0], 0, dtype=np.float)
for i in range(1, len(ts)):
      detrended[i] = ts[i] - ts[i-1]

crw = ConstrainedRandomWalk(ts[0:1000], int(z_vector_size), int(tau))
xs = crw.regenerate_time_series(int(regenerated_size))

np.savetxt(output_file, xs)
