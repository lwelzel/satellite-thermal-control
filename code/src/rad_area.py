import numpy as np
from scipy import optimize

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
area_radiator = 2.1 * 1.6

projected_front_area = 200.309
projected_side_area = 30.34
full_area = 424.3  # 424.3
sigma = 5.670e-8
# f_sun_1 = 0
# f_sun_2 = 1400

# 1 => reflector
# 2 => radome

f_sun1 = 0
f_sun2 = 1400
f_sun3 = 1400
projected_area = projected_front_area  # * np.cos(np.deg2rad(30))
f32 = 0.032
f23 = area_radiator / full_area * f32

#             T1^4      T2^4
# reflector
# radome



# sol = np.linalg.lstsq(m, s)
# sol = np.power(abs(sol[0]), 1 / 4)
#
# print(f"\tT_1: {sol[0]:.2f} K\n"
#       f"\tT_2: {sol[1]:.2f} K")

def func(x, A, v):
    y = np.dot(A, x) - v
    return np.dot(y, y)


def area_func(x):
    rad_a = area_radiator * x

    m = np.array([
        [
            (epsilon_reflector_out * full_area + epsilon_reflector_in * full_area) * sigma,
            - alpha_reflector_in * full_area * epsilon_radome_in * sigma,
            0
        ],

        [
            - alpha_radome_in * full_area * epsilon_reflector_in * sigma,
            (epsilon_radome_out * full_area + epsilon_radome_in * full_area) * sigma,
            - alpha_radome_out * full_area * f32 * epsilon_radiator * sigma
        ],

        [
            0,
            - alpha_radiator * rad_a * f23 * epsilon_radome_out * sigma,
            epsilon_radiator * rad_a * sigma
        ]
    ])

    s = np.array([
        alpha_reflector_out * projected_area * f_sun1,
        alpha_radome_out * projected_area * f_sun2,
        rad_a * alpha_radiator * np.cos(np.deg2rad(60)) * f_sun3 + 200
    ])

    bnds = ((2.7 ** 4, 1500 ** 4), (2.7 ** 4, 1500 ** 4), (273.0 ** 4, 305 ** 4))
    args = (m, s)
    # minimize the function with the given bounds
    res = optimize.minimize(func, x0=np.array([273.0 ** 4, 273.0 ** 4, 285.0 ** 4]),
                            args=args, method='SLSQP', bounds=bnds,
                            tol=1e-8,
                            options={'disp': False})
    sol = np.power(res.x, 1 / 4)
    return abs(sol[2] - 298.0)

bnds1 = ((0., 1.))
# minimize the function with the given bounds
res1 = optimize.minimize(area_func, x0=np.array([0.5]),
                        method='SLSQP', bounds=bnds1,
                        tol=1e-8,
                        options={'disp': False})

print(f"\tDifference vector : {res1.x - 298.0 }, should be very small.")

sol = res1.x
print(f"\A_f: {sol:.3f}")
