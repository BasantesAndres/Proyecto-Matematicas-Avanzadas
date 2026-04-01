import numpy as np
from euler import euler
from rk4 import rk4
from rkf45 import rkf45
from problems import problem1
from metrics import error_infty, error_l2


def main():
    prob = problem1()

    # Euler y RK4 con paso fijo
    h = 0.1
    sol_euler = euler(prob.f, prob.t0, prob.y0, prob.T, h)
    sol_rk4 = rk4(prob.f, prob.t0, prob.y0, prob.T, h)

    y_ex_euler = prob.exact(sol_euler.t)
    y_ex_rk4 = prob.exact(sol_rk4.t)

    print("=== Problem 1 ===")
    print("Euler")
    print("  nfev       =", sol_euler.nfev)
    print("  error_inf  =", error_infty(y_ex_euler, sol_euler.y))
    print("  error_l2   =", error_l2(y_ex_euler, sol_euler.y, sol_euler.h))

    print("RK4")
    print("  nfev       =", sol_rk4.nfev)
    print("  error_inf  =", error_infty(y_ex_rk4, sol_rk4.y))
    print("  error_l2   =", error_l2(y_ex_rk4, sol_rk4.y, sol_rk4.h))

    # RKF45 adaptativo
    sol_rkf = rkf45(
        prob.f,
        prob.t0,
        prob.y0,
        prob.T,
        TOL=1e-6,
        h_max=0.1,
        h_min=1e-8,
        h0=1e-3
    )

    y_ex_rkf = prob.exact(sol_rkf.t)

    print("RKF45")
    print("  nfev       =", sol_rkf.nfev)
    print("  accepted   =", sol_rkf.n_accept)
    print("  rejected   =", sol_rkf.n_reject)
    print("  status     =", sol_rkf.status)
    print("  error_inf  =", error_infty(y_ex_rkf, sol_rkf.y))


if __name__ == "__main__":
    main()