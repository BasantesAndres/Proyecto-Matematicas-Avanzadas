import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def _ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def _is_scalar(y0):
    y0_arr = np.asarray(y0, dtype=float)
    return y0_arr.ndim == 0


def plot_solution_by_method(problem, t_ref, y_ref, solutions, method_name, outdir, filename_prefix):
    """
    solutions: lista de dicts con
        {
            "label": str,
            "t": array,
            "y": array
        }
    """
    _ensure_dir(outdir)
    scalar = _is_scalar(problem.y0)
    method_tag = method_name.lower()

    if scalar:
        plt.figure(figsize=(8, 5))
        plt.plot(t_ref, y_ref, "k--", linewidth=2, label="Exacta / referencia")

        for sol in solutions:
            plt.plot(sol["t"], sol["y"], marker="o", markersize=3, linewidth=1.2, label=sol["label"])

        plt.xlabel("t")
        plt.ylabel("y(t)")
        plt.title(f"Solución - {problem.name} - {method_name}")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(Path(outdir) / f"{filename_prefix}_solution_{method_tag}.png", dpi=150)
        plt.close()

    else:
        y_ref = np.asarray(y_ref)
        m = y_ref.shape[1]

        for j in range(m):
            plt.figure(figsize=(8, 5))
            plt.plot(t_ref, y_ref[:, j], "k--", linewidth=2, label=f"Referencia comp. {j+1}")

            for sol in solutions:
                yj = np.asarray(sol["y"])[:, j]
                plt.plot(sol["t"], yj, marker="o", markersize=3, linewidth=1.2, label=sol["label"])

            plt.xlabel("t")
            plt.ylabel(f"Componente {j+1}")
            plt.title(f"Solución - {problem.name} - {method_name} - comp. {j+1}")
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.tight_layout()
            plt.savefig(Path(outdir) / f"{filename_prefix}_solution_{method_tag}_comp{j+1}.png", dpi=150)
            plt.close()


def plot_pointwise_error_by_method(problem, error_curves, method_name, outdir, filename_prefix):
    """
    error_curves: lista de dicts con
        {
            "label": str,
            "t": array,
            "err": array
        }
    """
    _ensure_dir(outdir)
    method_tag = method_name.lower()

    plt.figure(figsize=(8, 5))
    for curve in error_curves:
        plt.semilogy(curve["t"], curve["err"], linewidth=1.5, label=curve["label"])

    plt.xlabel("t")
    plt.ylabel("Error puntual")
    plt.title(f"Error puntual - {problem.name} - {method_name}")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(Path(outdir) / f"{filename_prefix}_pointwise_error_{method_tag}.png", dpi=150)
    plt.close()


def plot_convergence(problem, hs, errors_euler, errors_rk4, outdir, filename_prefix):
    _ensure_dir(outdir)

    plt.figure(figsize=(8, 5))
    plt.loglog(hs, errors_euler, "o-", linewidth=1.5, label="Euler")
    plt.loglog(hs, errors_rk4, "s-", linewidth=1.5, label="RK4")
    plt.xlabel("h")
    plt.ylabel("Error infinito")
    plt.title(f"Convergencia - {problem.name}")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(Path(outdir) / f"{filename_prefix}_convergence.png", dpi=150)
    plt.close()


def plot_efficiency(problem, data, outdir, filename_prefix):
    _ensure_dir(outdir)

    plt.figure(figsize=(8, 5))
    for method, (nfevs, errors) in data.items():
        plt.loglog(nfevs, errors, "o-", linewidth=1.5, label=method)

    plt.xlabel("Número de evaluaciones de f")
    plt.ylabel("Error infinito")
    plt.title(f"Eficiencia - {problem.name}")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(Path(outdir) / f"{filename_prefix}_efficiency.png", dpi=150)
    plt.close()


def plot_adaptive_steps(problem, t, h_hist, outdir, filename_prefix):
    _ensure_dir(outdir)

    plt.figure(figsize=(8, 5))
    plt.step(t[:-1], h_hist, where="post")
    plt.xlabel("t")
    plt.ylabel("h_n")
    plt.title(f"Pasos adaptativos RKF45 - {problem.name}")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(Path(outdir) / f"{filename_prefix}_adaptive_steps.png", dpi=150)
    plt.close()


def plot_phase_plane(problem, y, outdir, filename_prefix):
    _ensure_dir(outdir)

    y = np.asarray(y)
    if y.ndim != 2 or y.shape[1] < 2:
        raise ValueError("La gráfica de plano fase requiere un sistema de al menos 2 componentes.")

    plt.figure(figsize=(6, 6))
    plt.plot(y[:, 0], y[:, 1], linewidth=1.5)
    plt.xlabel("x(t)")
    plt.ylabel("y(t)")
    plt.title(f"Plano fase - {problem.name}")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(Path(outdir) / f"{filename_prefix}_phase_plane.png", dpi=150)
    plt.close()


def plot_stability_problem2(problem, t_ref, y_ref, solution_sets, outdir, filename_prefix):
    _ensure_dir(outdir)

    plt.figure(figsize=(8, 5))
    plt.plot(t_ref, y_ref, "k--", linewidth=2, label="Exacta")

    for sol in solution_sets:
        plt.plot(sol["t"], sol["y"], marker="o", markersize=3, linewidth=1.2, label=sol["label"])

    plt.xlabel("t")
    plt.ylabel("y(t)")
    plt.title(f"Experimento de estabilidad - {problem.name}")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(Path(outdir) / f"{filename_prefix}_stability.png", dpi=150)
    plt.close()