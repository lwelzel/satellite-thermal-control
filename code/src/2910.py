import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt

alpha_radome_in = 1
alpha_radome_out = alpha_radome_in
alpha_reflector_in = 1
alpha_reflector_out = 0.14

epsilon_radome_in = 1
epsilon_radome_out = epsilon_radome_in
epsilon_reflector_in = 1
epsilon_reflector_out = 0.045

epsilon_radiator = 0.78
alpha_radiator = 0.13
area_radiator = 2.1 * 1.6 * 0.425

projected_front_area = 200.309
projected_side_area = 30.34
full_area = 424.3 / 2
sigma = 5.670e-8
# f_sun_1 = 0
# f_sun_2 = 1400

# 1 => reflector
# 2 => radome

f_sun1 = 1400
f_sun2 = 1400
f_sun3 = 0
projected_area = projected_front_area * np.cos(np.deg2rad(55))
f32 = 0.032
f23 = area_radiator / full_area * f32

from scipy import interpolate

#             T1^4      T2^4
# reflector
# radome

n = 100

critical_area = projected_front_area * np.cos(np.deg2rad(55))

# x1 = np.array([*x, *x1])
# y1 = np.array([*y, *y1])
# x2 = x1
# y2 = np.flip(y1)

x1 = np.linspace(0, 90, n, endpoint=True)
y1 = projected_front_area * np.cos(np.deg2rad(x1))
_x1 = np.linspace(0, 55, n, endpoint=False)
_y1 = projected_front_area * np.cos(np.deg2rad(_x1))

xx1 = [55, 90, 180-55]
yy1 = [critical_area, projected_side_area, 0]
interpolate1 = interpolate.interp1d(xx1, yy1, kind='quadratic',
                                    bounds_error=False, fill_value="extrapolate")
xx1 = np.linspace(0, 180, n, endpoint=True)
yy1 = interpolate1(xx1)

__x1 = np.linspace(55, 180, n, endpoint=False)
__y1 = np.where(__x1 < 180-55, interpolate1(__x1), 0)
_x1 = np.array([*_x1, *__x1])
_y1 = np.array([*_y1, *__y1])


xx2 = [55, 90, 180-55]
yy2 = [0, projected_side_area, critical_area]
interpolate2 = interpolate.interp1d(xx2, yy2, kind='quadratic',
                                    bounds_error=False, fill_value="extrapolate")
xx2 = np.linspace(0, 180, n, endpoint=True)
yy2 = interpolate2(xx2)

_x2 = np.linspace(0, 180-55, n, endpoint=False)
_y2 = np.where(_x2>55, interpolate2(_x2), 0)

x2 = np.linspace(90, 180, n, endpoint=True)
y2 = projected_front_area * np.cos(np.deg2rad(x2 - 180))

__x2 = np.linspace(180-55, 180, n, endpoint=False)
__y2 = projected_front_area * np.cos(np.deg2rad(__x2 - 180))

_x2 = np.array([*_x2, *__x2])
_y2 = np.array([*_y2, *__y2])

_x = np.linspace(0, 180, n, endpoint=True)
interp1 = interpolate.interp1d(_x1, _y1, kind="quadratic", bounds_error=False, fill_value="extrapolate")
interp2 = interpolate.interp1d(_x2, _y2, kind="quadratic", bounds_error=False, fill_value="extrapolate")

y_tot = interp1(_x) + interp2(_x)


fig, ax = plt.subplots(nrows=1, ncols=1,
                         constrained_layout=True,
                         # sharex=True, # sharey=True,
                         figsize=(12, 6))

ax.scatter(x1, y1, label=r"Reflector Proj.: $\propto cos(\alpha)$", c="darkred", marker="^", s=40, alpha=0.5)
ax.scatter(xx1, yy1, label=r"Reflector Crit.: quadratic spline", c="darkred", marker="*", s=40, alpha=0.5)
ax.scatter(x2, y2, label=r"Radome Proj.: $\propto cos(\alpha - 180^\circ)$", c="darkblue", marker="+", s=40, alpha=0.5)
ax.scatter(xx2, yy2, label=r"Radome Crit.: quadratic spline", c="darkblue", marker=".", s=40, alpha=0.5)

ax.plot(_x1, _y1, label="Reflector Area", c="darkred")
ax.plot(_x2, _y2, label="Radome Area", c="darkblue")
ax.plot(_x, y_tot, label="Total Area", c="purple", linewidth=2)

ax.axhline(critical_area, ls="dashed", c="gray", label=r"$A_{crit} \approx 115~m^2$")

ax.axvline(90, ls="dotted", c="gray")
ax.axvline(180-55, ls="dotted", c="gray")
ax.axvline(55, ls="dotted", c="gray")

ax.set_ylim(0, 220)
ax.set_xlim(0, 180)

ax.set_xlabel(r'$\alpha$ [$^\circ$]')
ax.set_title("Exposed Antenna Area")
ax.set_ylabel(r'$A$ [$m^2$]')
ax.legend()
fig.suptitle(r'SC Temperature - Areas', fontsize=20)
plt.show()

dissipation = np.linspace(200, 600, n)
angles = np.linspace(0, 180, n)

temps = np.zeros((n, n, 3))

for i, angle in enumerate(angles):
    projected_area1 = interp1(angle)
    projected_area2 = interp2(angle)

    f32 = 0.032
    f23 = area_radiator / full_area * f32

    for j, p_diss in enumerate(dissipation):
        m = np.array([
            [
                (epsilon_reflector_out * full_area + epsilon_reflector_in * full_area) * sigma,
                - epsilon_reflector_in * full_area * epsilon_radome_in * sigma,
                0
            ],

            [
                - epsilon_radome_in * full_area * epsilon_reflector_in * sigma,
                (epsilon_radome_out * full_area + epsilon_radome_in * full_area) * sigma,
                - epsilon_radome_out * full_area * f23 * epsilon_radiator * sigma
            ],

            [
                0,
                - epsilon_radiator * area_radiator * f32 * epsilon_radome_out * sigma,
                epsilon_radiator * area_radiator * sigma
            ]
        ])

        s = np.array([
            alpha_reflector_out * projected_area1 * f_sun1,
            alpha_radome_out * projected_area2 * f_sun2,
            p_diss # area_radiator * alpha_radiator * np.cos(np.deg2rad(60)) * f_sun3 + 200
        ])

        sol = np.linalg.lstsq(m, s)
        sol = np.power(sol[0], 1 / 4)

        # print(f"\tT_1: {sol[0]:.2f} K\n"
        #       f"\tT_2: {sol[1]:.2f} K\n"
        #       f"\tT_3: {sol[2]:.2f} K")


        def func(x, A, v):
            y = np.dot(A, x) - v
            return np.dot(y, y)

        # print(f"\tDifference vector : {np.dot(m, sol**4.) - s}, should be very small.")


        bnds = ((2.7 ** 4, 1500. ** 4.), (2.7 ** 4, 1500. ** 4.), (2.7 ** 4., 1500. ** 4.))
        args = (m, s)
        # minimize the function with the given bounds
        rng = np.random.default_rng()
        # noise = rng.normal(0, 1e-2, 3)
        res = optimize.minimize(func, x0=(sol)**4.,
                                args=args, method='SLSQP', bounds=bnds,
                                options={'disp': False, "ftol":1e-30})

        sol = np.power(res.x, 1 / 4) - 273.15

        temps[j, i] = sol
        # print(f"\tT_1: {sol[0]:.2f} K\n"
        #       f"\tT_2: {sol[1]:.2f} K\n"
        #       f"\tT_3: {sol[2]:.2f} K")
        # print(f"\tDifference vector : {np.dot(m, res.x) - s}, should be very small.")

fig, axes = plt.subplots(nrows=1, ncols=3,
                         constrained_layout=True,
                         # sharex=True, # sharey=True,
                         figsize=(14, 4))
titles = ["Reflector", "Radome", "Radiator"]
levels = [[100], [100], [10, 25]]

from mpl_toolkits.axes_grid1 import make_axes_locatable
import seaborn as sns

plt.rcParams.update({'hatch.color': 'w'})

def fmt(x):
    s = f"{x:.0f}"+r"$^\circ C$"
    return s

poss = [
    [(150, 412)], [(150, 412)], [(91, 490), (100, 400)]
]

for i, (ax, title, level, pos) in enumerate(zip(axes.flatten(), titles, levels, poss)):
    im = ax.imshow(temps[:, :, i],
                   origin="lower",
                   extent=[0, 180, 200, 600],
                   aspect=(180)/400,
                   vmin=-60, vmax=120,
                   interpolation='bilinear')

    c1 = ax.contour(temps[:, :, i], levels=level,
                         colors="w", origin="lower", extent=[0, 180, 200, 600],
                         linestyles="dashed")

    ax.clabel(c1, fontsize=10, inline=True, colors='w', fmt=fmt, manual=pos)

    plt.colorbar(im, ax=ax, label=r'Temperature [$^\circ C$]',
                 fraction=0.046, pad=0.04)

    if i < 2:
        c1 = ax.contour(temps[:, :, 2], levels=[-100, 10, 25, 150],
                             colors="w", origin="lower", extent=[0, 180, 200, 600],
                             linestyles="-", linewidths=0.7)
    c1 = ax.contourf(angles, dissipation, temps[:, :, 2],
                     levels=[-100, 10, 25, 150],
                     hatches=["\\", None, "\\"],
                     colors="none",
                     origin="lower", extent=[0, 180, 200, 600],
                     alpha=0)

    ax.text(5, 440, "Operations", ha="left", va="center", c="w", size=10)
    ax.text(170, 412, "Curing", ha="center", va="center", c="w", size=10, rotation=90)

    ax.set_xlabel(r'$\alpha$ [$^\circ$]')
    ax.set_title(title)
    ax.set_ylim(200, 600)
    ax.set_ylabel(r'$Q_{3, ~tot}$ [$W$]')

print(np.max(temps[:, :, 0]), np.max(temps[:, :, 1]), np.max(temps[:, :, 2]))



fig.suptitle(r'SC Temperature - Systems', fontsize=20)
plt.show()

