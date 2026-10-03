from time import perf_counter
from constants import NormalizedModelData, print_stats, print_breakline


# =========================================================
# EFFICIENCY
# =========================================================

def parameter_efficiency(d: NormalizedModelData) -> float:  # objective
    efficiency: float = d["parameter"] / d["storage"]
    return efficiency


def context_efficiency(d: NormalizedModelData) -> float:  # objective
    efficiency: float = d["context"] / d["storage"]
    return efficiency


def additive_normalized_efficiency(d: NormalizedModelData) -> float:  # subjective
    efficiency: float = (d["parameter_normalized"] + d["context_normalized"]) / d["storage"]
    return efficiency


def multiplicative_normalized_efficiency(d: NormalizedModelData) -> float:  # subjective
    efficiency: float = (d["parameter_normalized"] * d["context_normalized"]) / d["storage"]
    return efficiency


# =========================================================
# DOMINATION
# =========================================================

def dominates_3var(a: NormalizedModelData, b: NormalizedModelData) -> bool:  # uses: parameter, context, storage
    return (a["parameter"] >= b["parameter"] and a["context"] >= b["context"] and a["storage"] <= b["storage"] and (a["parameter"] > b["parameter"] or a["context"] > b["context"] or a["storage"] < b["storage"]))


def dominates_2var(a: NormalizedModelData, b: NormalizedModelData) -> bool:  # uses: parameter/storage, context/storage
    return (a["parameter_efficiency"] >= b["parameter_efficiency"] and a["context_efficiency"] >= b["context_efficiency"] and (a["parameter_efficiency"] > b["parameter_efficiency"] or a["context_efficiency"] > b["context_efficiency"]))


# =========================================================
# PARETO FRONTIER
# =========================================================

def pareto_frontier_3var(data: list[NormalizedModelData]) -> list[NormalizedModelData]:
    frontier: list[NormalizedModelData] = []

    for model in data:
        dominated: bool = False

        for other in data:
            if model != other and dominates_3var(other, model):
                dominated = True
                break

        if not dominated:
            frontier.append(model)

    return frontier


def pareto_frontier_2var(data: list[NormalizedModelData]) -> list[NormalizedModelData]:
    frontier: list[NormalizedModelData] = []

    for model in data:
        dominated: bool = False

        for other in data:
            if model != other and dominates_2var(other, model):
                dominated = True
                break

        if not dominated:
            frontier.append(model)

    return frontier


# =========================================================
# COMPARE DATA
# =========================================================

def comparing_main(data: list[NormalizedModelData], print_best_models_3var: bool = False, print_best_models_2var: bool = False, print_clean_models: bool = False, comparing_debug: bool = False) -> list[NormalizedModelData]:
    start_time: float = perf_counter()

    for d in data:
        d["parameter_efficiency"] = parameter_efficiency(d)
        d["context_efficiency"] = context_efficiency(d)
        d["additive_normalized_efficiency"] = additive_normalized_efficiency(d)
        d["multiplicative_normalized_efficiency"] = multiplicative_normalized_efficiency(d)

    if print_clean_models:
        print(f"{'full_name':<30} | {'parameter':<10} | {'parameter_normalized':<20} | {'parameter_efficiency':<20} | {'context':<10} | {'context_normalized':<20} | {'context_efficiency':<20} | {'storage':<10} | {'additive_normalized_efficiency':<30} | {'multiplicative_normalized_efficiency':<35}")
        print("-" * 220)

        for d in data:
            print(f"{d['full_name']:<30} | {d['parameter']:<10} | {d['parameter_normalized']:<20.5f} | {d['parameter_efficiency']:<20.2f} | {d['context']:<10} | {d['context_normalized']:<20.5f} | {d['context_efficiency']:<20.2f} | {d['storage']:<10.2f} | {d['additive_normalized_efficiency']:<30.5f} | {d['multiplicative_normalized_efficiency']:<35.5f}")

    result: list[NormalizedModelData] = data

    if print_best_models_3var:
        result = pareto_frontier_3var(data)
        result.sort(key=lambda x: x["multiplicative_normalized_efficiency"], reverse=True)

        print(f"{'full_name':<30} | {'parameter':<10} | {'context':<10} | {'storage':<10} | {'additive_normalized':<20} | {'multiplicative_normalized':<25}")
        print("-" * 120)

        for d in result:
            print(f"{d['full_name']:<30} | {d['parameter']:<10} | {d['context']:<10} | {d['storage']:<10.2f} | {d['additive_normalized_efficiency']:<20.5f} | {d['multiplicative_normalized_efficiency']:<25.5f}")

        print(f"3-Var Pareto Frontier: {len(result)} models")

    elif print_best_models_2var:
        result = pareto_frontier_2var(data)
        result.sort(key=lambda x: x["multiplicative_normalized_efficiency"], reverse=True)

        print(f"{'full_name':<30} | {'parameter/storage':<20} | {'context/storage':<20} | {'additive_normalized':<20} | {'multiplicative_normalized':<25}")
        print("-" * 120)

        for d in result:
            print(f"{d['full_name']:<30} | {d['parameter_efficiency']:<20.2f} | {d['context_efficiency']:<20.2f} | {d['additive_normalized_efficiency']:<20.5f} | {d['multiplicative_normalized_efficiency']:<25.5f}")

        print(f"2-Var Pareto Frontier: {len(result)} models")

    if comparing_debug:
        print_breakline(80)
        print_stats(f"Comparing duration: {perf_counter() - start_time:.2f} seconds")
        print_breakline(80)

    return result