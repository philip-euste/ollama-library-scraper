from time import perf_counter
from constants import ModelData, NormalizedModelData, print_stats, print_breakline

# =========================================================
# NORMALIZE VARIANT
# =========================================================

def normalize_variants(variant: str) -> float:
    first: str = variant.split("-")[0]

    if first.endswith("b"):
        return float(first[:-1])

    elif first.endswith("m"):
        return float(first[:-1]) / 1000

    raise ValueError(f"Unknown variant: {variant}")


# =========================================================
# NORMALIZE STORAGE
# =========================================================

def normalize_storage(storage: str | None) -> float | None:
    if storage is None:
        return None

    if "-" in storage:
        storage = storage.split("-")[-1].strip()

    if storage.endswith("TB"):
        return float(storage[:-2]) * 1000

    elif storage.endswith("GB"):
        return float(storage[:-2])

    elif storage.endswith("MB"):
        return float(storage[:-2]) / 1000

    raise ValueError(f"Unknown storage: {storage}")


# =========================================================
# NORMALIZE CONTEXT
# =========================================================

def normalize_context(context: str) -> float:
    if context.endswith("M"):
        return float(context[:-1]) * 1000

    elif context.endswith("K"):
        return float(context[:-1])

    raise ValueError(f"Unknown context: {context}")


# =========================================================
# NORMALIZE FEATURE
# =========================================================

def normalize_feature(data: list[NormalizedModelData], key: str) -> None:
    values: list[float] = [model[key] for model in data]

    minimum: float = min(values)
    maximum: float = max(values)

    for model in data:
        model[key + "_normalized"] = (model[key] - minimum) / (maximum - minimum) # there shouldn't be 0


# =========================================================
# NORMALIZE DATA
# =========================================================

def normalizing_main(data: list[ModelData], normalize_debug: bool = False) -> list[NormalizedModelData]:
    start_time: float = perf_counter()
    normalized_data: list[NormalizedModelData] = []

    for model in data:
        storage: float | None = normalize_storage(model["storage"])

        if storage is None:
            raise ValueError(f"Missing storage for model: {model['full_name']}")

        context: float = normalize_context(model["context"]) if model["context"] is not None else 0.0
        parameter: float = normalize_variants(model["variant"]) if model["variant"] is not None else 0.0

        normalized_model: NormalizedModelData = {
    "full_name": model["full_name"],
    "family": model["family"],
    "variant": model["variant"],
    "storage": storage,
    "context": context,
    "capabilities": model["capabilities"],
    "modalities": model["modalities"],
    "parameter": parameter,
    "parameter_normalized": 0.0,
    "context_normalized": 0.0,
    "parameter_efficiency": 0.0,
    "context_efficiency": 0.0,
    "additive_normalized_efficiency": 0.0,
    "multiplicative_normalized_efficiency": 0.0,
}

        normalized_data.append(normalized_model)

    normalize_feature(normalized_data, "parameter")
    normalize_feature(normalized_data, "context")

    if normalize_debug:
        print_breakline(80)
        print_stats(f"Normalizing duration: {perf_counter() - start_time:.2f} seconds")
        print_breakline(80)


    return normalized_data