import numpy as np
import matplotlib.pyplot as plt


angle1 = np.linspace(30, 90, 100)  # rotation about y axis
angle2 = np.linspace(0, 90, 100)  # rotation about x axis

a1, a2 = np.meshgrid(angle1, angle2)

def illuminated_single_radiator_surface_usat(ang1, ang2, width=2.1, height=1.6, rad_angle=np.deg2rad(30)):
    ang1 = np.deg2rad(ang1)
    ang2 = np.deg2rad(ang2)
    area = width * height
    return area * np.clip(np.sin(ang1 + rad_angle), a_min=0, a_max=1) * np.cos(ang2)

def illuminated_radiator_surface_usat(ang1, ang2, width=2.1, height=1.6, rad_angle=np.deg2rad(30)):
    ang1 = np.deg2rad(ang1)
    ang2 = np.deg2rad(ang2)
    area = width * height
    return area * ((np.clip(np.sin(ang1-30), a_min=0, a_max=None)) + np.clip(np.sin(ang1+30), a_min=0, a_max=None))



fig, ax = plt.subplots(nrows=1, ncols=1,
                       constrained_layout=True,
                       # sharex=True, sharey=True,
                       figsize=(6, 6))

area = illuminated_single_radiator_surface_usat(a1, a2)

h = plt.contourf(angle1, angle2, area)
plt.colorbar()

# ax.set_ylim(2.9, 3.4)
# ax.set_xlabel(r'Pointing angle [$^\circ$]')
# ax.set_ylabel(r'Exposed radiator area [$m^2$]')

ax.set_xlabel(r'rotation about y axis')
ax.set_ylabel(r'rotation about x axis')
ax.set_title(r'Exposed radiator area vs. SC pointing angle w.r.t. sun')
fig.suptitle(r'SC radiator illumination', fontsize=20)
plt.show()