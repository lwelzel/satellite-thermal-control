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

projected_front_area = 200.309
projected_side_area = 30.34
full_area = 424.3 / 2  # 424.3
sigma = 5.670e-8
# f_sun_1 = 0
# f_sun_2 = 1400

# 1 => reflector
# 2 => radome

cases_outer = ["AL reflector outside", "AL reflector inside"]
a_ref_ins = [1, 0.14]
a_ref_outs = [0.14, 1]
e_ref_ins = [1, 0.045]
e_ref_outs = [0.045, 1]

cases = ["0 DEG - from radome", "90 DEG - from side", "180 DEG - from reflector"]
f_sun_1 = [0, 1400, 1400]
f_sun_2 = [1400, 1400, 0]
projected_areas = [projected_front_area, projected_side_area, projected_front_area]

for case_outer, alpha_reflector_in, alpha_reflector_out, epsilon_reflector_in, epsilon_reflector_out in zip(cases_outer,
                                                                                                            a_ref_ins,
                                                                                                            a_ref_outs,
                                                                                                            e_ref_ins,
                                                                                                            e_ref_outs):
    print(f"====================>>>\n{case_outer}")
    for case, f_sun1, f_sun2, projected_area in zip(cases, f_sun_1, f_sun_2, projected_areas):
        print(f"\t====================>>>\n\t{case}")

        #             T1^4      T2^4
        # reflector
        # radome

        m = np.array([
            [
                (epsilon_reflector_out * full_area + epsilon_reflector_in * full_area) * sigma,
                - epsilon_reflector_in * full_area * epsilon_radome_in * sigma
            ],

            [
                - epsilon_radome_in * full_area * epsilon_reflector_in * sigma,
                (epsilon_radome_out * full_area + epsilon_radome_in * full_area) * sigma,

            ]
        ])

        s = np.array([
            alpha_reflector_out * projected_area * f_sun1,
            alpha_radome_out * projected_area * f_sun2
        ])


        # sol = np.linalg.lstsq(m, s)
        # sol = np.power(abs(sol[0]), 1 / 4)
        #
        # print(f"\tT_1: {sol[0]:.2f} K\n"
        #       f"\tT_2: {sol[1]:.2f} K")

        def func(x, A, v):
            y = np.dot(A, x) - v
            return np.dot(y, y)


        bnds = ((2.7 ** 4, 1500 ** 4), (2.7 ** 4, 1500 ** 4))
        args = (m, s)
        # minimize the function with the given bounds
        res = optimize.minimize(func, x0=np.array([400.0 ** 4, 400.0 ** 4]),
                                args=args, method='SLSQP', bounds=bnds,
                                tol=1e-8,
                                options={'disp': False})
        print(f"\tDifference vector : {np.dot(m, res.x) - s}, should be very small.")

        sol = np.power(res.x, 1 / 4)
        print(f"\tT_1: {sol[0]:.2f} K\n"
              f"\tT_2: {sol[1]:.2f} K")

        print(f"\tDelta T {np.abs(sol[0] - sol[1]):.2f} K")
