from time import perf_counter

from constants import print_stats, print_breakline, ModelData, FG, FR

# =========================================================
# CLEAN DATA
# =========================================================

def cleaning_main(data: list[ModelData], debug_cleaned_rejected: bool = False, debug_cleaned_accepted: bool = False) -> list[ModelData]:

    start_time: float = perf_counter()

    accepted: list[ModelData] = []
    rejected: list[ModelData] = []

    banned_families: tuple[str, ...] = ("bge", "embed")
    banned_variants: tuple[str, ...] = ("cloud", "latest", "mlx", "x", "q", "fp")

    def rejection_print(model: ModelData) -> None:
        rejected.append(model)

        if debug_cleaned_rejected:
            print_stats(f"REJECTED: {model}", FR)

    for model in data:
        variant: str | None = model["variant"]
        family: str = model["family"]
        storage: str | None = model["storage"]
        capabilities: list[str] = model["capabilities"]

        if variant is None:
            rejection_print(model)
            continue

        if any(word in variant.lower() for word in banned_variants):
            rejection_print(model)
            continue

        if any(word in family.lower() for word in banned_families):
            rejection_print(model)
            continue

        if storage is None:
            rejection_print(model)
            continue

        if variant.startswith("e"):
            rejection_print(model)
            continue

        first: str = variant.split("-")[0]

        if not (first.endswith("b") or first.endswith("m")):
            rejection_print(model)
            continue

        if "embedding" in capabilities:
            rejection_print(model)
            continue

        accepted.append(model)

        if debug_cleaned_accepted:
            print_stats(f"ACCEPTED: {model}", FG)

    print_breakline(80)
    print_stats(f"Total Uncleaned Data: {len(data)}")
    print_stats(f"Accepted Data: {len(accepted)}", FG)
    print_stats(f"Rejected Data: {len(rejected)}", FR)
    print_stats(f"Cleaning duration: {perf_counter() - start_time:.2f} seconds")
    print_breakline(80)

    return accepted