import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

import pandas as pd

df = pd.read_csv('temu_session_statistics_w_id_25.5.17.csv')

"""
df.head()
     duration  fpackets  bpackets  fbytes   bbytes  label  id
0    0.508558        24        19    3870    13807  18403   0
1    0.489827        18        13    2198     5354  18403   1
2  147.612398       108       126   24271    82981  17403   2
3  147.316961       615       728   58336   880828  18403   3
4    3.607463       964      1259   83446  1757394  17403   4
"""

plt.figure()
df.plot(x='id',y='duration', title='duration')
df.plot(x='id',y='fpackets', title='fpackets')
df.plot(x='id',y='bpackets', title='bpackets')
df.plot(x='id',y='fbytes', title='fbytes')
df.plot(x='id',y='bbytes', title='bbytes')
df.hist(column='duration', bins=1000)
plt.title('duration hitogram')
plt.show()
