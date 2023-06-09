import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import scienceplots
import matplotlib.animation as animation
plt.style.use(["science"])
plt.rcParams["font.size"] = "10.5"
plt.rcParams['savefig.bbox'] = 'tight' 

flow = np.load('data/wake_vort.npy')
xlims, ylims = (1, 2), (-0.35, 0.35)
print("Loaded")
nx, ny, nt = flow.shape
pxs = np.linspace(xlims[0], xlims[1], nx)
pys = np.linspace(ylims[0], ylims[1], ny)

nframes = nt//4
fn = 'wake'
lim=[-0.005, 0.005]

flow = np.load('data/fluctuations.npy')

sec = flow.reshape(nx, ny, nt)[:,:,:nframes]
fig, ax = plt.subplots(figsize=(5, 4))
levels = np.linspace(lim[0], lim[1], 44)
_cmap = sns.color_palette("seismic", as_cmap=True)

cont = ax.contourf(pxs, pys, sec[:,:,0].T,
                            levels=levels,
                            vmin=lim[0],
                            vmax=lim[1],
                            # norm=norm,
                            cmap=_cmap,
                            extend="both",
                        )

ax.set_aspect(1)
ax.set(xlabel=r"$x$", ylabel=r"$y$")#, title=r"$\phi_{" + str(m) + r"}$")


def animate(i):
    global cont
    for c in cont.collections:
        c.remove()
    cont = plt.contourf(pxs, pys, sec[:,:,i].T,
                            levels=levels,
                            vmin=lim[0],
                            vmax=lim[1],
                            # norm=norm,
                            cmap=_cmap,
                            extend="both",
                        )
    return cont.collections

anim = animation.FuncAnimation(fig, animate, frames=nframes, interval=50, blit=True, repeat=False)

anim.save(f"./figures/{fn}.gif", fps=100, bitrate=-1, dpi=400)