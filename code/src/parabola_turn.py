import numpy as np
import matplotlib.pyplot as plt


length = np.linspace(-15.97/2, 15.97/2, 300)

turning = np.deg2rad(55)


def rotate(point, origin = np.array([0,0]), angle=np.deg2rad(30)):
    ox, oy = origin
    px, py = point

    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    return np.array([qx, qy])

def parabola(x, pm=1):
    return - pm * 0.0446987 * x**2 + pm * 5.7/2

fig, ax = plt.subplots(nrows=1, ncols=1,
                       constrained_layout=True, subplot_kw={'aspect': 1},
                       # sharex=True, sharey=True,
                       figsize=(8, 8))

p1 = parabola(length)
p1 = np.vstack((length, p1))
p1 = rotate(p1, angle=turning)

p2 = parabola(length, -1)
p2 = np.vstack((length, p2))
p2 = rotate(p2, angle=turning)

min = np.min((p1[1], p2[1]))
p1[1] += -min
p2[1] += -min

ax.plot(*p1, c="k", ls="dashed", label="Radome")
ax.plot(*p2, c="k", ls="dashed")

ax.plot(length, parabola(length), c="gray", ls="dashed", alpha=0.7)
ax.plot(length, parabola(length, -1), c="gray", ls="dashed", alpha=0.7)

ax.fill_between(*p2,
                hatch='||', facecolor="none", alpha=0.5,
                label="Sun Illumination")

l = np.cos(turning) * 15.97/2
ax.plot([-l, +l], [0, 0], c="r", label="flat projection diameter")


ax.axvline(0, c="k", ls="dotted")

middle = np.max(p1[1])/2

sc_h = 2 * 1.4
x_sc = np.linspace(0, sc_h, 100)

y_sc = x_sc * np.cos(turning) + middle + np.cos(turning) * 5.7/2
x_sc = - x_sc * np.sin(turning) - np.sin(turning) * 5.7/2

pspace =  np.linspace(5, -7, 1000) # np.linspace(x_sc.min(), x_sc.max(), 100)
p3 = parabola(pspace)
p3 = np.vstack((pspace, p3))
p3 = rotate(p3, angle=turning)
p3[1] += -min

ax.plot(x_sc,
        y_sc, c="orange", label="SC height above antenna")

p3 = np.interp(x_sc, np.flip(p3[0]), np.flip(p3[1]), left=0, right=0)

ax.fill_between(x_sc,
                y_sc,
                np.where(p3 > 0., p3, 0),
                hatch='||', ec="yellow", fc="none", alpha=0.5,
                label="SC Sun Illumination")



ax.set_xlim(-10, 10)
ax.set_ylim(None, np.max(p1[1]) * 1.2)
ax.legend()

ax.set_xlabel(r'Original SC y-axis [$m$]')
ax.set_ylabel(r'Original SC x-direction [$m$]')

ax.set_title(r'Approximation of the radome shape is $y \approx \pm * 0.045 x^2 \pm 2.85 ~[m]$')
fig.suptitle(r'Illumination of the Antenna $\alpha=55^\circ$', fontsize=20)
plt.show()