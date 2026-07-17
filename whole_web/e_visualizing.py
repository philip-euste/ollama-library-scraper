from matplotlib import pyplot as plt

from a_scraping import threading_web_data
from b_cleaning import cleaning_data
from c_normalizing import normalize_data
from d_comparing import comparing_data

data = normalize_data(cleaning_data(threading_web_data()))

frontier = comparing_data(data, PRINT_BEST_MODELS_2VAR=True)
# frontier = comparing_data(data, PRINT_BEST_MODELS_3VAR=True)
print(f"{'full_name':<30} | {'parameter':<10} | {'parameter_normalized':<10} | {'parameter_efficiency':<10} | {'context':<10} | {'context_normalized':<10} | {'context_efficiency':<10} | {'storage':<10} | {'additive_normalized_efficiency':<10} | {'multiplicative_normalized_efficiency':<10}")

for d in frontier:
    print(f"{d['full_name']:<30} | {d['parameter']:<10} | {d['parameter_normalized']:<10.5f} | {d['parameter_efficiency']:<10.2f} | {d['context']:<10} | {d['context_normalized']:<10.5f} | {d['context_efficiency']:<10.2f} | {d['storage']:<10.2f} | {d['additive_normalized_efficiency']:<10.5f} | {d['multiplicative_normalized_efficiency']:<10.5f}")



def plot_2d_efficiency(data, frontier):
    x = [d["parameter_efficiency"] for d in data]
    y = [d["context_efficiency"] for d in data]

    fx = [d["parameter_efficiency"] for d in frontier]
    fy = [d["context_efficiency"] for d in frontier]

    plt.figure(figsize=(10, 6))

    plt.scatter(x, y, s=20, label="All Models")
    plt.scatter(fx, fy, s=60, label="Pareto Frontier")

    for d in frontier:
        plt.annotate(
            d["full_name"],
            (
                d["parameter_efficiency"],
                d["context_efficiency"]
            ),
            fontsize=8
        )

    plt.xlabel("Parameter Efficiency (B parameters / GB)")
    plt.ylabel("Context Efficiency (K context / GB)")
    plt.title("Ollama Models: Storage Efficiency Pareto Frontier")

    plt.xscale("log")
    plt.yscale("log")

    plt.grid(True)
    plt.legend()

    plt.show()


plot_2d_efficiency(data, frontier)