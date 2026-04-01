import numpy as np
from rk4 import rk4
from rkf45 import rkf45
from metrics import interpolate_reference


def compute_reference(problem, method="rk4"):
    """
    Si hay solución exacta, la usa.
    Si no la hay:
    - RK4 con h=1e-4
    - o RKF45 con TOL=1e-10
    """
    if problem.exact is not None:
        t_ref = np.linspace(problem.t0, problem.T, 5000)
        y_ref = problem.exact(t_ref)
        return t_ref, y_ref

    if method.lower() == "rk4":
        sol = rk4(problem.f, problem.t0, problem.y0, problem.T, h=1e-4)
        return sol.t, sol.y

    if method.lower() == "rkf45":
        sol = rkf45(
            problem.f,
            problem.t0,
            problem.y0,
            problem.T,
            TOL=1e-10,
            h_max=0.1,
            h_min=1e-12,
            h0=1e-3
        )
        return sol.t, sol.y

    raise ValueError("Método de referencia no reconocido. Usa 'rk4' o 'rkf45'.")


def reference_on_grid(problem, t_query, method="rk4"):
    if problem.exact is not None:
        return problem.exact(t_query)

    t_ref, y_ref = compute_reference(problem, method=method)
    return interpolate_reference(t_ref, y_ref, t_query)