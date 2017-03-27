import sys, argparse
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

pd.options.display.max_rows = 40
pd.options.display.expand_frame_repr = False
# sns.set(style="ticks", palette="pastel", color_codes=True) ##Make sure this line come before mpl.rc changes
mpl.rc('text', usetex=True)
mpl.rc('font',**{'family': 'serif', 'serif': ['Computer Modern']})  ##make sure come after import seaborn and seaborn.set
color_map = plt.cm.Set1(np.linspace(0, 1, 9))

pd.options.display.max_rows = 40
pd.options.display.expand_frame_repr = False


# df = pd.read_csv("/home/alek/Desktop/Example/LCT.src.out")
df = pd.read_csv("/home/alek/PycharmProjects/iSAFE/example/demo.isafe.out")

# ba_pos = 136608646 #LCT
ba_pos = 2500000 #demo
# ba_pos = 38798648 #TLR1
# ba_pos = 48258198 #ABCC11
# ba_pos = 159174683 # ACKR1

I = df["id"]==ba_pos
x = "id"
# x = "freq"
y = "isafe"
plt.plot(df[x], df[y], '.')
plt.plot(df.loc[I, x], df.loc[I, y], 'ro')
