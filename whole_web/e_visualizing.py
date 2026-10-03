from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from typing import cast
from mpl_toolkits.mplot3d import Axes3D

from d_comparing import comparing_main
from constants import NormalizedModelData


# =========================================================
# PRINT FRONTIER
# =========================================================

def print_frontier(frontier: list[NormalizedModelData]) -> None:
    print(f"{'full_name':<30} | {'parameter':<10} | {'parameter_normalized':<20} | {'parameter_efficiency':<20} | {'context':<10} | {'context_normalized':<20} | {'context_efficiency':<20} | {'storage':<10} | {'additive_normalized_efficiency':<30} | {'multiplicative_normalized_efficiency':<35}")

    for d in frontier:
        print(f"{d['full_name']:<30} | {d['parameter']:<10} | {d['parameter_normalized']:<20.5f} | {d['parameter_efficiency']:<20.2f} | {d['context']:<10} | {d['context_normalized']:<20.5f} | {d['context_efficiency']:<20.2f} | {d['storage']:<10.2f} | {d['additive_normalized_efficiency']:<30.5f} | {d['multiplicative_normalized_efficiency']:<35.5f}")


# =========================================================
# PLOT 2D EFFICIENCY
# =========================================================

def plot_2d_efficiency(data: list[NormalizedModelData], frontier: list[NormalizedModelData]) -> None:
    x: list[float] = [d["parameter_efficiency"] for d in data]
    y: list[float] = [d["context_efficiency"] for d in data]

    fx: list[float] = [d["parameter_efficiency"] for d in frontier]
    fy: list[float] = [d["context_efficiency"] for d in frontier]

    plt.figure(figsize=(10, 6))

    plt.scatter(x, y, s=20, label="All Models")
    plt.scatter(fx, fy, s=60, label="Pareto Frontier")

    for d in frontier:
        plt.annotate(d["full_name"], (d["parameter_efficiency"], d["context_efficiency"]), fontsize=8)

    plt.xlabel("Parameter Efficiency (B parameters / GB)")
    plt.ylabel("Context Efficiency (K context / GB)")
    plt.title("Ollama Models: Storage Efficiency Pareto Frontier")

    plt.xscale("log")
    plt.yscale("log")

    plt.grid(True)
    plt.legend()

    plt.show()

# ==# =========================================================
# PLOT 3D FRONTIER
# =========================================================

def plot_3d_frontier(data: list[NormalizedModelData], frontier: list[NormalizedModelData]) -> None:
    figure: Figure = plt.figure(figsize=(10, 8))
    axes: Axes3D = cast(Axes3D, figure.add_subplot(111, projection="3d"))
    
    x: list[float] = [d["parameter"] for d in data]
    y: list[float] = [d["storage"] for d in data]
    z: list[float] = [d["context"] for d in data]

    fx: list[float] = [d["parameter"] for d in frontier]
    fy: list[float] = [d["storage"] for d in frontier]
    fz: list[float] = [d["context"] for d in frontier]

    axes.scatter(xs=x, ys=y, zs=z, s=20, label="All Models")  # type: ignore[arg-type]
    axes.scatter(xs=fx, ys=fy, zs=fz, s=60, label="Pareto Frontier")  # type: ignore[arg-type]
    
    for d in frontier:
        axes.text(d["parameter"], d["storage"], d["context"], d["full_name"], fontsize=8)

    axes.set_xlabel("Parameters (B)")
    axes.set_ylabel("Storage (GB)")
    axes.set_zlabel("Context (K)")
    axes.set_title("Ollama Models: 3-Variable Pareto Frontier")

    axes.legend()

    plt.show()

# =========================================================
# VISUALIZING MAIN
# =========================================================

def visualizing_main(data: list[NormalizedModelData], variable_count: int = 2, comparing_debug: bool = False) -> list[NormalizedModelData]:

    # -----------------------------------------------------
    # PROCESS DATA
    # -----------------------------------------------------

    if variable_count == 2:
        frontier: list[NormalizedModelData] = comparing_main(data, print_best_models_2var = True, comparing_debug = comparing_debug)

    elif variable_count == 3:
        frontier: list[NormalizedModelData] = comparing_main(data, print_best_models_3var = True, comparing_debug = comparing_debug)

    else:
        raise ValueError(f"Unknown variable count: {variable_count}")

    # -----------------------------------------------------
    # PRINT FRONTIER
    # -----------------------------------------------------

    print_frontier(frontier)

    # -----------------------------------------------------
    # VISUALIZATIONS
    # -----------------------------------------------------

    if variable_count == 2:
        plot_2d_efficiency(data, frontier)

    elif variable_count == 3:
        plot_3d_frontier(data, frontier)

    return frontier