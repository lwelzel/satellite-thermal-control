import numpy as np
import matplotlib.pyplot as plt


length = np.linspace(-15.97/2, 15.97/2, 300)

def parabola(x, pm=1):
    return - pm * 0.0446987 * x**2 + pm * 5.7/2

fig, ax = plt.subplots(nrows=1, ncols=1,
                       constrained_layout=True, subplot_kw={'aspect': 1},
                       # sharex=True, sharey=True,
                       figsize=(12, 5))

ax.plot(length, parabola(length), c="k", ls="dashed", label="Radome")
ax.plot(length, parabola(length, -1), c="k", ls="dashed")

ax.fill_between(length, parabola(length), parabola(length, -1), hatch='\\\\', facecolor="none", alpha=0.5,
                label="Radome cross-section")
ax.axhline(0, c="k", ls="dotted")
ax.axvline(0, c="k", ls="dotted")
ax.text(-9.9, 0 - 0.1, 'Torus\ncenter',
        horizontalalignment='left',
        verticalalignment='top',)

ax.text(0.1, - 3.5, 'SC x-axis',
        horizontalalignment='left',
        verticalalignment='bottom',)

ax.set_xlim(-10, 10)
ax.set_ylim(- 3.5, None)
ax.legend()

ax.set_xlabel(r'SC y-axis [$m$]')
ax.set_ylabel(r'SC x-direction [$m$]')

ax.set_title(r'Approximation of the radome shape is $y \approx \pm * 0.045 x^2 \pm 2.85 ~[m]$')
fig.suptitle(r'Side view of the radome', fontsize=20)
plt.show()