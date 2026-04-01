from pathlib import Path

from problems import (
    problem2,
    problem3,
    problem4,
    problem5_sin,
    problem5_pulse,
)

from experiments import (
    run_solution_and_error_plots,
    run_convergence_study,
    run_efficiency_study,
    run_adaptive_step_plot,
    run_phase_plane,
    run_stability_experiment_problem2,
)


def main():
    base_out = Path("outputs")
    base_out.mkdir(exist_ok=True)

    # =========================
    # PROBLEMAS SINTÉTICOS (sin problem1)
    # =========================
    p2 = problem2(k=100.0)
    p3 = problem3()

    for prob in [p2, p3]:
        outdir = base_out / prob.name
        print(f"Procesando {prob.name} ...")

        # solución y error separados por método
        run_solution_and_error_plots(
            prob,
            outdir=outdir,
            N_values=(50, 100, 200),
            rkf_tols=(1e-4, 1e-6, 1e-8),
            include_rkf=True
        )

        run_convergence_study(prob, outdir=outdir)
        run_efficiency_study(prob, outdir=outdir)

    # estabilidad solo para problem2
    print("Procesando experimento de estabilidad del problema 2 ...")
    run_stability_experiment_problem2(p2, outdir=base_out / p2.name)

    # pasos adaptativos problem2
    run_adaptive_step_plot(p2, outdir=base_out / p2.name)

    # =========================
    # MALWARE
    # =========================
    malware_problems = [
        problem4(1.5, 0.5),
        problem4(1.0, 0.5),
        problem4(0.8, 0.6),
    ]

    for prob in malware_problems:
        outdir = base_out / prob.name
        print(f"Procesando {prob.name} ...")

        run_solution_and_error_plots(
            prob,
            outdir=outdir,
            N_values=(100, 200),
            rkf_tols=(1e-6,),
            include_rkf=True
        )

        run_adaptive_step_plot(prob, outdir=outdir)

    # =========================
    # BALANCEO DE CARGA
    # aquí solo referencia + Euler(N=100,200) y referencia + RK4(N=100,200)
    # =========================
    balance_problems = [
        problem5_sin(),
        problem5_pulse(),
    ]

    for prob in balance_problems:
        outdir = base_out / prob.name
        print(f"Procesando {prob.name} ...")

        run_solution_and_error_plots(
            prob,
            outdir=outdir,
            N_values=(100, 200),
            rkf_tols=(),
            include_rkf=False
        )

        run_adaptive_step_plot(prob, outdir=outdir)
        run_phase_plane(prob, outdir=outdir)

    print("Todo listo. Revisa la carpeta outputs/")


if __name__ == "__main__":
    main()