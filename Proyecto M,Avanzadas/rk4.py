import numpy as np
from dataclasses import dataclass


@dataclass
class ODESolution:
    t: np.ndarray
    y: np.ndarray
    h: float
    nfev: int


def _prepare_state(y0):
    y0_arr = np.asarray(y0, dtype=float)
    is_scalar = (y0_arr.ndim == 0)
    y0_arr = np.atleast_1d(y0_arr).astype(float)
    return y0_arr, is_scalar


def _format_output(y, is_scalar):
    if is_scalar:
        return y[:, 0]
    return y


def rk4(f, t0, y0, T, h):
    """
    Método clásico de Runge-Kutta de orden 4 para PVI escalar o sistema:
        u'(t) = f(t, u),   u(t0) = u0
    """
    if h <= 0:
        raise ValueError("h debe ser positiva.")
    if T <= t0:
        raise ValueError("Se espera T > t0.")

    y0_arr, is_scalar = _prepare_state(y0)

    N = int(np.round((T - t0) / h))
    if N <= 0:
        raise ValueError("El número de pasos N debe ser positivo.")

    h = (T - t0) / N
    t = np.linspace(t0, T, N + 1)
    y = np.zeros((N + 1, len(y0_arr)), dtype=float)
    y[0] = y0_arr

    nfev = 0
    for n in range(N):
        tn = t[n]
        yn = y[n]

        k1 = np.atleast_1d(np.asarray(f(tn, yn), dtype=float))
        k2 = np.atleast_1d(np.asarray(f(tn + h/2, yn + (h/2)*k1), dtype=float))
        k3 = np.atleast_1d(np.asarray(f(tn + h/2, yn + (h/2)*k2), dtype=float))
        k4 = np.atleast_1d(np.asarray(f(tn + h, yn + h*k3), dtype=float))

        if not (k1.shape == k2.shape == k3.shape == k4.shape == yn.shape):
            raise ValueError("f(t, y) devolvió una dimensión incompatible.")

        y[n + 1] = yn + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
        nfev += 4

    return ODESolution(
        t=t,
        y=_format_output(y, is_scalar),
        h=h,
        nfev=nfev
    )