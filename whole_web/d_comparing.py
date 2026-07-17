def parameter_efficiency(d): # objective
    efficiency = d['parameter'] / d['storage']
    return efficiency

def context_efficiency(d): # objective
    efficiency = d['context'] / d['storage']
    return efficiency

def additive_normalized_efficiency(d): # subjective
    efficiency = (d['parameter_normalized'] + d['context_normalized']) / d['storage']
    return efficiency

def multiplicative_normalized_efficiency(d): # subjective
    efficiency = (d['parameter_normalized'] * d['context_normalized']) / d['storage']
    return efficiency

def dominates_3var(a, b): # uses: parameter, context, storage
    return (a["parameter"] >= b["parameter"] and a["context"] >= b["context"] and a["storage"] <= b["storage"] and (a["parameter"] > b["parameter"] or a["context"] > b["context"] or a["storage"] < b["storage"]))

def dominates_2var(a, b): # uses: parameter/ storage, context/ storage
    return (a["parameter_efficiency"] >= b["parameter_efficiency"] and a["context_efficiency"] >= b["context_efficiency"] and (a["parameter_efficiency"] > b["parameter_efficiency"]or a["context_efficiency"] > b["context_efficiency"]))

def pareto_frontier_3var(data):
    frontier = []

    for model in data:
        dominated = False

        for other in data:
            if model != other and dominates_3var(other, model):
                dominated = True
                break

        if not dominated:
            frontier.append(model)

    return frontier

def pareto_frontier_2var(data):
    frontier = []

    for model in data:
        dominated = False

        for other in data:
            if model != other and dominates_2var(other, model):
                dominated = True
                break

        if not dominated:
            frontier.append(model)

    return frontier

def comparing_data(data, PRINT_CLEAN_MODELS = False, PRINT_BEST_MODELS_3VAR = False, PRINT_BEST_MODELS_2VAR = False):
    for d in data:
        d['parameter_efficiency'] = parameter_efficiency(d)
        d['context_efficiency'] = context_efficiency(d)
        d['additive_normalized_efficiency'] = additive_normalized_efficiency(d)
        d['multiplicative_normalized_efficiency'] = multiplicative_normalized_efficiency(d) # upscale for readability

    if PRINT_CLEAN_MODELS:
        print(f"{'full_name':<30} | {'parameter':<10} | {'parameter_normalized':<10} | {'parameter_efficiency':<10} | {'context':<10} | {'context_normalized':<10} | {'context_efficiency':<10} | {'storage':<10} | {'additive_normalized_efficiency':<10} | {'multiplicative_normalized_efficiency':<10}")
        print("-" * 120)

        for d in data:
            print(f"{d['full_name']:<30} | {d['parameter']:<10} | {d['parameter_normalized']:<10.5f} | {d['parameter_efficiency']:<10.2f} | {d['context']:<10} | {d['context_normalized']:<10.5f} | {d['context_efficiency']:<10.2f} | {d['storage']:<10.2f} | {d['additive_normalized_efficiency']:<10.5f} | {d['multiplicative_normalized_efficiency']:<10.5f}")

    if PRINT_BEST_MODELS_3VAR:
        best_models_3var = pareto_frontier_3var(data)
        best_models_3var.sort(key=lambda x: x["multiplicative_normalized_efficiency"], reverse=True)
        print(f"{'full_name':<30} | {'parameter':<10} | {'context':<10} | {'storage':<10} | {'additive_normalized':<20} | {'multiplicative_normalized':<25}")
        print("-" * 120)
        for d in best_models_3var:
            print(f"{d["full_name"]:<30} | {d['parameter']:<10} | {d['context']:<10} | {d['storage']:<10} | {d['additive_normalized_efficiency']:<10.5f} | {d['multiplicative_normalized_efficiency']:<10.5f}")

        print(f"Objectively Best 3-Var Data: {len(best_models_3var)}")
        return best_models_3var

    if PRINT_BEST_MODELS_2VAR:
        best_models_2var = pareto_frontier_2var(data)
        best_models_2var.sort(key=lambda x: x["multiplicative_normalized_efficiency"], reverse=True)
        print(f"{'full_name':<30} | {'parameter/storage':<20} | {'context/storage':<20} | {'additive_normalized':<20} | {'multiplicative_normalized':<25}")
        print("-" * 120)

        for d in best_models_2var:
            print(f"{d["full_name"]:<30} | {d['parameter_efficiency']:<10.2f} | {d['context_efficiency']:<10.2f} | {d['additive_normalized_efficiency']:<10.5f} | {d['multiplicative_normalized_efficiency']:<10.5f}")

        print(f"Objectively Best 2-Var Data: {len(best_models_2var)}")
        return best_models_2var
    
    return data