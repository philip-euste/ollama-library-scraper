from colorama import Fore

def cleaning_data(data):
    accepted = []
    rejected = []

    BANNED_FAMILIES = ["bge", "embed"]
    BANNED_VARIANTS = ["cloud", "latest", "mlx", 'x', 'q', 'fp']

    PRINT_REJECTED = False
    PRINT_ACCEPTED = False

    def rejection_print(d):
        rejected.append(d)
        if PRINT_REJECTED:
            print(f"{Fore.LIGHTRED_EX}REJECTED:{Fore.RESET} {d}")
    for d in data:
        if any(word in d["variant"].lower() for word in BANNED_VARIANTS): # quantized, cloud, latest, mlx, expert-mixed
            rejection_print(d)
            continue
        if any(word in d["family"].lower() for word in BANNED_FAMILIES): # embedding families
            rejection_print(d)
            continue
        if d['storage'] is None: # cloud storages
            rejection_print(d)
            continue
        if d['variant'].startswith("e"): # expert parameters
            rejection_print(d)
            continue

        first = d['variant'].split("-")[0]

        if not (first.endswith("b") or first.endswith("m")): # others
            rejection_print(d)
            continue

        if 'embedding' in d['capabilities']: # embedding
            rejection_print(d)
            continue
        
        accepted.append(d)
        if PRINT_ACCEPTED:
            print(f"{Fore.LIGHTGREEN_EX}ACCEPTED:{Fore.RESET} {d}")

    print(f"Total Uncleaned Data: {len(data)}")
    print(f"Accepted Data: {len(accepted)}")
    print(f"Rejected Data: {len(rejected)}")

    return accepted
