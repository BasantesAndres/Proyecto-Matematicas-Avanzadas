import math
import numpy as np
from dataclasses import dataclass


@dataclass
class AdaptiveODESolution:
    t: np.ndarray
    y: np.ndarray
    h_hist: np.ndarray
    nfev: int
    n_accept: int
    n_reject: int
    status: str
    message: str


def _prepare_state(y0):
    y0_arr = np.asarray(y0, dtype=float)
    is_scalar = (y0_arr.ndim == 0)
    y0_arr = np.atleast_1d(y0_arr).astype(float)
    return y0_arr, is_scalar


def _format_output(y, is_scalar):
    if is_scalar:
        return y[:, 0]
    return y


def _error_norm(e, is_scalar):
    if is_scalar:
        return abs(float(e[0]))
    return np.linalg.norm(e, ord=2)


def rkf45(
    f,
    t0,
    y0,
    T,
    TOL=1e-6,
    h_max=0.1,
    h_min=1e-10,
    h0=None,
    conservative=True,
    clip=(0.1, 4.0),
    use_pi=True,
    alpha=1/5,
    beta=0.04,
    max_steps=200000,
):
    """
    RKF45 adaptativo para escalar o sistema.
    Usa el valor de orden 5 como solución aceptada.
    """
    if TOL <= 0:
        raise ValueError("TOL debe ser positiva.")
    if h_max <= 0 or h_min <= 0:
        raise ValueError("h_max y h_min deben ser positivos.")
    if T <= t0:
        raise ValueError("Se espera T > t0.")

    y0_arr, is_scalar = _prepare_state(y0)

    direction = 1.0
    h_max_signed = direction * abs(h_max)
    h_min_mag = abs(h_min)

    if h0 is None:
        h = h_max_signed
    else:
        h = direction * min(abs(h0), abs(h_max))
        if h == 0.0:
            h = h_max_signed

    t_hist = [float(t0)]
    y_hist = [y0_arr.copy()]
    h_hist = []

    t = float(t0)
    w = y0_arr.copy()

    nfev = 0
    n_accept = 0
    n_reject = 0
    status = "success"
    message = "Reached T."

    p = 4
    theta = 0.84 if conservative else 1.0
    qmin, qmax = clip
    R_prev = None

    steps = 0
    while t < T:
        steps += 1
        if steps > max_steps:
            status = "max_steps_exceeded"
            message = "Maximum number of steps exceeded."
            break

        if abs(h) > abs(T - t):
            h = T - t
            if h == 0.0:
                break

        K1 = h * np.atleast_1d(np.asarray(f(t, w), dtype=float))
        K2 = h * np.atleast_1d(np.asarray(f(t + (1/4)*h, w + (1/4)*K1), dtype=float))
        K3 = h * np.atleast_1d(np.asarray(f(t + (3/8)*h, w + (3/32)*K1 + (9/32)*K2), dtype=float))
        K4 = h * np.atleast_1d(np.asarray(
            f(t + (12/13)*h, w + (1932/2197)*K1 - (7200/2197)*K2 + (7296/2197)*K3),
            dtype=float
        ))
        K5 = h * np.atleast_1d(np.asarray(
            f(t + h, w + (439/216)*K1 - 8*K2 + (3680/513)*K3 - (845/4104)*K4),
            dtype=float
        ))
        K6 = h * np.atleast_1d(np.asarray(
            f(t + (1/2)*h, w - (8/27)*K1 + 2*K2 - (3544/2565)*K3 + (1859/4104)*K4 - (11/40)*K5),
            dtype=float
        ))

        if not (K1.shape == K2.shape == K3.shape == K4.shape == K5.shape == K6.shape == w.shape):
            raise ValueError("f(t, y) devolvió una dimensión incompatible.")

        nfev += 6

        w4 = w + (25/216)*K1 + (1408/2565)*K3 + (2197/4104)*K4 - (1/5)*K5
        w5 = w + (16/135)*K1 + (6656/12825)*K3 + (28561/56430)*K4 - (9/50)*K5 + (2/55)*K6

        err_vec = (w5 - w4) / h if h != 0 else np.full_like(w, np.inf)
        R = _error_norm(err_vec, is_scalar)

        if R <= TOL:
            t_new = t + h
            w_new = w5

            t_hist.append(float(t_new))
            y_hist.append(w_new.copy())
            h_hist.append(abs(h))

            t = float(t_new)
            w = w_new.copy()
            n_accept += 1

            if (R > 0.0) and math.isfinite(R):
                if use_pi and (R_prev is not None and R_prev > 0.0):
                    q = theta * (TOL / R)**alpha * (R_prev / TOL)**beta
                else:
                    q = theta * (TOL / R)**(1/p)
            else:
                q = qmax

            q = max(qmin, min(q, qmax))
            h = q * h

            if abs(h) > abs(h_max_signed):
                h = math.copysign(abs(h_max_signed), h)

            if math.isfinite(R) and R > 0.0:
                R_prev = R

        else:
            n_reject += 1

            if (R > 0.0) and math.isfinite(R):
                if use_pi and (R_prev is not None and R_prev > 0.0):
                    q = theta * (TOL / R)**alpha * (R_prev / TOL)**beta
                else:
                    q = theta * (TOL / R)**(1/p)
            else:
                q = qmin

            q = max(qmin, min(q, qmax))
            h = q * h

            if abs(h) > abs(h_max_signed):
                h = math.copysign(abs(h_max_signed), h)

            if abs(h) < h_min_mag:
                status = "hmin_exceeded"
                message = "Minimum step h_min exceeded during reattempt."
                break

            if math.isfinite(R) and R > 0.0:
                R_prev = R

    Y = np.vstack(y_hist)

    return AdaptiveODESolution(
        t=np.array(t_hist, dtype=float),
        y=_format_output(Y, is_scalar),
        h_hist=np.array(h_hist, dtype=float),
        nfev=nfev,
        n_accept=n_accept,
        n_reject=n_reject,
        status=status,
        message=message
    )