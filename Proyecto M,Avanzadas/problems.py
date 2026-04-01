import numpy as np
from dataclasses import dataclass
from typing import Callable, Optional, Any


@dataclass
class Problem:
    name: str
    t0: float
    T: float
    y0: Any
    f: Callable
    exact: Optional[Callable] = None
    description: str = ""


def problem1():
    """
    y'(t) = -2y(t) + sin(t),   y(0)=1,   t in [0,10]
    Exact:
    y(t) = (2/5) sin(t) - (1/5) cos(t) + (6/5)e^{-2t}
    """
    def f(t, y):
        return -2.0 * y + np.sin(t)

    def exact(t):
        t = np.asarray(t, dtype=float)
        return (2/5) * np.sin(t) - (1/5) * np.cos(t) + (6/5) * np.exp(-2*t)

    return Problem(
        name="problem1",
        t0=0.0,
        T=10.0,
        y0=1.0,
        f=f,
        exact=exact,
        description="y'=-2y+sin(t), y(0)=1"
    )


def problem2(k=100.0):
    """
    y'(t) = k / (1 + (k(t-1))^2),   y(0)=arctan(-k),   t in [0,5]
    Exact:
    y(t) = arctan(k(t-1))
    """
    def f(t, y):
        return k / (1.0 + (k*(t - 1.0))**2)

    def exact(t):
        t = np.asarray(t, dtype=float)
        return np.arctan(k*(t - 1.0))

    return Problem(
        name="problem2",
        t0=0.0,
        T=5.0,
        y0=np.arctan(-k),
        f=f,
        exact=exact,
        description=f"y'=k/(1+(k(t-1))^2), y(0)=arctan(-k), k={k}"
    )


def problem3():
    """
    x' = y
    y' = -x - 0.2y
    x(0)=1, y(0)=0, t in [0,20]
    """
    omega = np.sqrt(0.99)

    def f(t, u):
        x, y = u
        return np.array([y, -x - 0.2*y], dtype=float)

    def exact(t):
        t = np.asarray(t, dtype=float)
        x = np.exp(-0.1*t) * (np.cos(omega*t) + (0.1/omega)*np.sin(omega*t))
        y = -(1.0/omega) * np.exp(-0.1*t) * np.sin(omega*t)

        if t.ndim == 0:
            return np.array([x, y], dtype=float)

        return np.column_stack((x, y))

    return Problem(
        name="problem3",
        t0=0.0,
        T=20.0,
        y0=np.array([1.0, 0.0], dtype=float),
        f=f,
        exact=exact,
        description="Damped harmonic oscillator"
    )


def problem4(beta=1.5, gamma=0.5):
    """
    I' = beta*I*(1-I) - gamma*I
    I(0)=0.05, t in [0,20]
    """
    def f(t, I):
        return beta*I*(1.0 - I) - gamma*I

    return Problem(
        name=f"problem4_beta_{beta}_gamma_{gamma}",
        t0=0.0,
        T=20.0,
        y0=0.05,
        f=f,
        exact=None,
        description=f"Malware propagation, beta={beta}, gamma={gamma}"
    )


def problem5_sin():
    """
    x' = -ax + by + sin(t)
    y' = cx - dy
    """
    a, b, c, d = 1.2, 0.4, 0.3, 0.9

    def forcing(t):
        return np.sin(t)

    def f(t, u):
        x, y = u
        return np.array([
            -a*x + b*y + forcing(t),
            c*x - d*y
        ], dtype=float)

    return Problem(
        name="problem5_sin",
        t0=0.0,
        T=20.0,
        y0=np.array([1.0, 0.0], dtype=float),
        f=f,
        exact=None,
        description="Load balancing with f(t)=sin(t)"
    )


def problem5_pulse():
    """
    x' = -ax + by + f(t)
    y' = cx - dy
    con:
    f(t)=2 si 0<=t<=5
    f(t)=0 si t>5
    """
    a, b, c, d = 1.2, 0.4, 0.3, 0.9

    def forcing(t):
        return 2.0 if 0.0 <= t <= 5.0 else 0.0

    def f(t, u):
        x, y = u
        return np.array([
            -a*x + b*y + forcing(t),
            c*x - d*y
        ], dtype=float)

    return Problem(
        name="problem5_pulse",
        t0=0.0,
        T=20.0,
        y0=np.array([1.0, 0.0], dtype=float),
        f=f,
        exact=None,
        description="Load balancing with pulse input"
    )


def all_problems():
    return [
        problem1(),
        problem2(),
        problem3(),
        problem4(1.5, 0.5),
        problem4(1.0, 0.5),
        problem4(0.8, 0.6),
        problem5_sin(),
        problem5_pulse(),
    ]