import csv
import numpy as np
from pathlib import Path

from euler import euler
from rk4 import rk4
from rkf45 import rkf45

from metrics import pointwise_error, error_infty, estimate_orders
from reference_solutions import compute_reference, reference_on_grid

from plots import (
    plot_solution_by_method,
    plot_pointwise_error_by_method,
    plot_convergence,
    plot_efficiency,
    plot_adaptive_steps,
    plot_phase_plane,
    plot_stability_problem2,
)


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def save_csv(filepath, header, rows):
    ensure_dir(Path(filepath).parent)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def run_solution_and_error_plots(
    problem,
    outdir,
    N_values=(50, 100, 200),
    rkf_tols=(1e-4, 1e-6, 1e-8),
    include_rkf=True
):
    """
    Ahora genera gráficas SEPARADAS por método:
    - solution_euler
    - solution_rk4
    - solution_rkf45
    - pointwise_error_euler
    - pointwise_error_rk4
    - pointwise_error_rkf45
    """
    ensure_dir(outdir)

    t_ref, y_ref = compute_reference(problem, method="rk4")

    # ---------------- Euler ----------------
    euler_solutions = []
    euler_errors = []

    for N in N_values:
        h = (problem.T - problem.t0) / N
        sol_e = euler(problem.f, problem.t0, problem.y0, problem.T, h)
        y_true_e = reference_on_grid(problem, sol_e.t, method="rk4")
        err_e = pointwise_error(y_true_e, sol_e.y)

        euler_solutions.append({
            "label": f"Euler N={N}",
            "t": sol_e.t,
            "y": sol_e.y
        })
        euler_errors.append({
            "label": f"Euler N={N}",
            "t": sol_e.t,
            "err": err_e
        })

    plot_solution_by_method(
        problem=problem,
        t_ref=t_ref,
        y_ref=y_ref,
        solutions=euler_solutions,
        method_name="Euler",
        outdir=outdir,
        filename_prefix=problem.name
    )

    plot_pointwise_error_by_method(
        problem=problem,
        error_curves=euler_errors,
        method_name="Euler",
        outdir=outdir,
        filename_prefix=problem.name
    )

    # ---------------- RK4 ----------------
    rk4_solutions = []
    rk4_errors = []

    for N in N_values:
        h = (problem.T - problem.t0) / N
        sol_r = rk4(problem.f, problem.t0, problem.y0, problem.T, h)
        y_true_r = reference_on_grid(problem, sol_r.t, method="rk4")
        err_r = pointwise_error(y_true_r, sol_r.y)

        rk4_solutions.append({
            "label": f"RK4 N={N}",
            "t": sol_r.t,
            "y": sol_r.y
        })
        rk4_errors.append({
            "label": f"RK4 N={N}",
            "t": sol_r.t,
            "err": err_r
        })

    plot_solution_by_method(
        problem=problem,
        t_ref=t_ref,
        y_ref=y_ref,
        solutions=rk4_solutions,
        method_name="RK4",
        outdir=outdir,
        filename_prefix=problem.name
    )

    plot_pointwise_error_by_method(
        problem=problem,
        error_curves=rk4_errors,
        method_name="RK4",
        outdir=outdir,
        filename_prefix=problem.name
    )

    # ---------------- RKF45 ----------------
    if include_rkf and len(rkf_tols) > 0:
        rkf_solutions = []
        rkf_errors = []

        for tol in rkf_tols:
            sol_k = rkf45(
                problem.f,
                problem.t0,
                problem.y0,
                problem.T,
                TOL=tol,
                h_max=0.1,
                h_min=1e-8,
                h0=1e-3
            )
            y_true_k = reference_on_grid(problem, sol_k.t, method="rk4")
            err_k = pointwise_error(y_true_k, sol_k.y)

            rkf_solutions.append({
                "label": f"RKF45 tol={tol:.0e}",
                "t": sol_k.t,
                "y": sol_k.y
            })
            rkf_errors.append({
                "label": f"RKF45 tol={tol:.0e}",
                "t": sol_k.t,
                "err": err_k
            })

        plot_solution_by_method(
            problem=problem,
            t_ref=t_ref,
            y_ref=y_ref,
            solutions=rkf_solutions,
            method_name="RKF45",
            outdir=outdir,
            filename_prefix=problem.name
        )

        plot_pointwise_error_by_method(
            problem=problem,
            error_curves=rkf_errors,
            method_name="RKF45",
            outdir=outdir,
            filename_prefix=problem.name
        )


def run_convergence_study(problem, outdir, N_values=(50, 100, 200, 400, 800)):
    ensure_dir(outdir)

    hs = []
    errors_euler = []
    errors_rk4 = []

    for N in N_values:
        h = (problem.T - problem.t0) / N
        hs.append(h)

        sol_e = euler(problem.f, problem.t0, problem.y0, problem.T, h)
        y_true_e = reference_on_grid(problem, sol_e.t, method="rk4")
        errors_euler.append(error_infty(y_true_e, sol_e.y))

        sol_r = rk4(problem.f, problem.t0, problem.y0, problem.T, h)
        y_true_r = reference_on_grid(problem, sol_r.t, method="rk4")
        errors_rk4.append(error_infty(y_true_r, sol_r.y))

    orders_euler = estimate_orders(errors_euler)
    orders_rk4 = estimate_orders(errors_rk4)

    rows_euler = []
    rows_rk4 = []
    for i, N in enumerate(N_values):
        rows_euler.append([
            N,
            hs[i],
            errors_euler[i],
            "" if orders_euler[i] is None else orders_euler[i]
        ])
        rows_rk4.append([
            N,
            hs[i],
            errors_rk4[i],
            "" if orders_rk4[i] is None else orders_rk4[i]
        ])

    save_csv(
        Path(outdir) / f"{problem.name}_convergence_euler.csv",
        ["N", "h", "Error_Eh", "Estimated_Order"],
        rows_euler
    )
    save_csv(
        Path(outdir) / f"{problem.name}_convergence_rk4.csv",
        ["N", "h", "Error_Eh", "Estimated_Order"],
        rows_rk4
    )

    plot_convergence(
        problem=problem,
        hs=hs,
        errors_euler=errors_euler,
        errors_rk4=errors_rk4,
        outdir=outdir,
        filename_prefix=problem.name
    )


def run_efficiency_study(problem, outdir,
                         N_values=(50, 100, 200, 400, 800),
                         rkf_tols=(1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8)):
    ensure_dir(outdir)

    euler_nfev = []
    euler_err = []

    rk4_nfev = []
    rk4_err = []

    rkf_nfev = []
    rkf_err = []

    for N in N_values:
        h = (problem.T - problem.t0) / N

        sol_e = euler(problem.f, problem.t0, problem.y0, problem.T, h)
        y_true_e = reference_on_grid(problem, sol_e.t, method="rk4")
        euler_nfev.append(sol_e.nfev)
        euler_err.append(error_infty(y_true_e, sol_e.y))

        sol_r = rk4(problem.f, problem.t0, problem.y0, problem.T, h)
        y_true_r = reference_on_grid(problem, sol_r.t, method="rk4")
        rk4_nfev.append(sol_r.nfev)
        rk4_err.append(error_infty(y_true_r, sol_r.y))

    for tol in rkf_tols:
        sol_k = rkf45(
            problem.f,
            problem.t0,
            problem.y0,
            problem.T,
            TOL=tol,
            h_max=0.1,
            h_min=1e-10,
            h0=1e-3
        )
        y_true_k = reference_on_grid(problem, sol_k.t, method="rk4")
        rkf_nfev.append(sol_k.nfev)
        rkf_err.append(error_infty(y_true_k, sol_k.y))

    plot_efficiency(
        problem=problem,
        data={
            "Euler": (euler_nfev, euler_err),
            "RK4": (rk4_nfev, rk4_err),
            "RKF45": (rkf_nfev, rkf_err)
        },
        outdir=outdir,
        filename_prefix=problem.name
    )

    rows = []
    for nfev, err in zip(euler_nfev, euler_err):
        rows.append(["Euler", nfev, err])
    for nfev, err in zip(rk4_nfev, rk4_err):
        rows.append(["RK4", nfev, err])
    for nfev, err in zip(rkf_nfev, rkf_err):
        rows.append(["RKF45", nfev, err])

    save_csv(
        Path(outdir) / f"{problem.name}_efficiency.csv",
        ["Method", "nfev", "error_inf"],
        rows
    )


def run_adaptive_step_plot(problem, outdir, rkf_tol=1e-6):
    ensure_dir(outdir)

    sol_k = rkf45(
        problem.f,
        problem.t0,
        problem.y0,
        problem.T,
        TOL=rkf_tol,
        h_max=0.1,
        h_min=1e-10,
        h0=1e-3
    )

    plot_adaptive_steps(
        problem=problem,
        t=sol_k.t,
        h_hist=sol_k.h_hist,
        outdir=outdir,
        filename_prefix=problem.name
    )

    rows = []
    for i in range(len(sol_k.h_hist)):
        rows.append([sol_k.t[i], sol_k.t[i+1], sol_k.h_hist[i]])

    save_csv(
        Path(outdir) / f"{problem.name}_adaptive_steps.csv",
        ["t_left", "t_right", "h"],
        rows
    )


def run_phase_plane(problem, outdir, rkf_tol=1e-6):
    ensure_dir(outdir)

    sol_k = rkf45(
        problem.f,
        problem.t0,
        problem.y0,
        problem.T,
        TOL=rkf_tol,
        h_max=0.1,
        h_min=1e-10,
        h0=1e-3
    )

    plot_phase_plane(
        problem=problem,
        y=sol_k.y,
        outdir=outdir,
        filename_prefix=problem.name
    )


def run_stability_experiment_problem2(problem, outdir, h_values=(0.5, 0.25, 0.1)):
    ensure_dir(outdir)

    if problem.exact is None:
        raise ValueError("El experimento de estabilidad requiere una solución exacta o de referencia clara.")

    t_ref = np.linspace(problem.t0, problem.T, 3000)
    y_ref = problem.exact(t_ref)

    solutions = []

    for h in h_values:
        sol_e = euler(problem.f, problem.t0, problem.y0, problem.T, h)
        solutions.append({
            "label": f"Euler h={h}",
            "t": sol_e.t,
            "y": sol_e.y
        })

        sol_r = rk4(problem.f, problem.t0, problem.y0, problem.T, h)
        solutions.append({
            "label": f"RK4 h={h}",
            "t": sol_r.t,
            "y": sol_r.y
        })

    sol_k = rkf45(
        problem.f,
        problem.t0,
        problem.y0,
        problem.T,
        TOL=1e-6,
        h_max=0.5,
        h_min=1e-10,
        h0=1e-3
    )
    solutions.append({
        "label": "RKF45",
        "t": sol_k.t,
        "y": sol_k.y
    })

    plot_stability_problem2(
        problem=problem,
        t_ref=t_ref,
        y_ref=y_ref,
        solution_sets=solutions,
        outdir=outdir,
        filename_prefix=problem.name
    )