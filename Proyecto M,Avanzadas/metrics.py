import numpy as np


def pointwise_error(y_true, y_num):
    y_true = np.asarray(y_true, dtype=float)
    y_num = np.asarray(y_num, dtype=float)

    diff = y_true - y_num

    if diff.ndim == 1:
        return np.abs(diff)

    return np.linalg.norm(diff, axis=1)


def error_infty(y_true, y_num):
    return float(np.max(pointwise_error(y_true, y_num)))


def error_l2(y_true, y_num, h):
    y_true = np.asarray(y_true, dtype=float)
    y_num = np.asarray(y_num, dtype=float)

    diff = y_true - y_num

    if diff.ndim == 1:
        return float(np.sqrt(h * np.sum(diff**2)))

    row_norms = np.linalg.norm(diff, axis=1)
    return float(np.sqrt(h * np.sum(row_norms**2)))


def estimate_orders(errors):
    """
    Recibe una lista de errores [E_h1, E_h2, ...]
    y devuelve [None, p2, p3, ...]
    """
    orders = [None]
    for i in range(1, len(errors)):
        p = np.log(errors[i - 1] / errors[i]) / np.log(2.0)
        orders.append(float(p))
    return orders


def interpolate_reference(t_ref, y_ref, t_query):
    t_ref = np.asarray(t_ref, dtype=float)
    y_ref = np.asarray(y_ref, dtype=float)
    t_query = np.asarray(t_query, dtype=float)

    if y_ref.ndim == 1:
        return np.interp(t_query, t_ref, y_ref)

    out = np.zeros((len(t_query), y_ref.shape[1]), dtype=float)
    for j in range(y_ref.shape[1]):
        out[:, j] = np.interp(t_query, t_ref, y_ref[:, j])

    return out