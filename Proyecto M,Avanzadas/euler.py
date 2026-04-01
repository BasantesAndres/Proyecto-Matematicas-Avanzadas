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


def euler(f, t0, y0, T, h):
    """
    Método de Euler explícito para PVI escalar o sistema:
        u'(t) = f(t, u),   u(t0) = u0

    Parámetros
    ----------
    f  : función f(t, y)
    t0 : tiempo inicial
    y0 : condición inicial (escalar o vector)
    T  : tiempo final
    h  : paso deseado

    Retorna
    -------
    ODESolution con:
    - t    : malla temporal
    - y    : aproximación numérica
    - h    : paso real usado
    - nfev : número de evaluaciones de f
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
        fn = np.asarray(f(t[n], y[n]), dtype=float)
        fn = np.atleast_1d(fn)
        if fn.shape != y[n].shape:
            raise ValueError("f(t, y) devolvió una dimensión incompatible.")
        y[n + 1] = y[n] + h * fn
        nfev += 1

    return ODESolution(
        t=t,
        y=_format_output(y, is_scalar),
        h=h,
        nfev=nfev
    )