import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import plotly.plotly as py

py.sign_in('jonny2018', 'KhA9nBPkI28Gi2hlfe3K')

n = 50
x,y,z,s,ew = np.random.rand(5, n)
c,ec = np.random.rand(2,n,4)
area_scale, width_scale = 500, 5

fig, ax = plt.subplots()
sc = ax.scatter(x, y, c=c,
                s=np.square(s)*area_scale,
                edgecolor=ec,
                linewidth=ew*width_scale)
ax.grid

plt_url = py.plot_mpl(fig)
