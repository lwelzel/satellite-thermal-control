import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt

sigma = 5.670e-8
e_emissivity = 0.613  #????
e_albedo = 0.3

r_earth =  6371
pa = 6000 + r_earth
apa = 36000 + r_earth
mu = 3.986004418e14

a = (pa + apa) / 2

t_orbit = 2 * np.pi * np.sqrt((a*1000)**3 / mu)
t_ec = 45 * 60
e = (apa - pa) / (apa + pa )

t = np.linspace(0, t_orbit, 100)
eclipse = np.logical_and(t_orbit/2 - t_ec/2 < t, t < t_orbit/2 + t_ec/2)
s_flux = np.where(eclipse, 0, 1400)
theta = np.linspace(0, np.deg2rad(360), 100)
r_e = (a *(1-e**2)) / (1 + e * np.cos(theta))
e_flux = 285.**4 * sigma * e_emissivity
e_ir_flux = e_flux * r_earth**2/r_e**2
e_albedo_flux = 1400 * e_albedo * r_earth**2/r_e**2

fig, ax = plt.subplots(nrows=1, ncols=1,
                         constrained_layout=True,
                         # sharex=True, # sharey=True,
                         figsize=(12, 6))

ax.scatter(t/60, s_flux, label="Solar Flux", marker="+", color="darkred")
ax.set_xlabel(r'Time [$min$]')
ax.set_ylabel(r'Solar Flux [$W/m^2$]')
ax.set_title("Mission Orbit Parameters")
ax.legend()
fig.suptitle(r'SC - Battery Design', fontsize=20)
plt.show()

fig, ax = plt.subplots(nrows=1, ncols=1,
                         constrained_layout=True,
                         # sharex=True, # sharey=True,
                         figsize=(12, 6))

ax.scatter(np.rad2deg(theta), e_ir_flux, label="Earth IR Flux", marker="+", color="lightblue")
ax.scatter(np.rad2deg(theta), e_albedo_flux, label="Earth Albedo Flux", marker="^", color="darkblue")

ax.set_xlabel(r'Angle ($\theta$) [$^\circ$]')
ax.set_ylabel(r'Earth Flux [$W/m^2$]')
ax.set_title("Mission Orbit Parameters")
ax.legend()
fig.suptitle(r'SC - Battery Design', fontsize=20)
plt.show()