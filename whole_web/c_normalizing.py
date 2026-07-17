def normalize_variants(variant):
    first = variant.split("-")[0] # for 7b-v2 and 7b-v2.5

    if first.endswith("b"):
        return float(first[:-1])

    elif first.endswith("m"):
        return float(first[:-1]) / 1000
    
    raise ValueError(f"Unknown variant: {variant}")

def normalize_storage(storage):
    if storage.endswith("TB"):
        return float(storage[:-2]) * 1000
    
    elif storage.endswith("GB"):
        return float(storage[:-2])
    
    elif storage.endswith("MB"):
        return float(storage[:-2]) / 1000
    
    raise ValueError(f"Unknown storage: {storage}")

def normalize_context(context): # readability > optimization
    if context.endswith("M"):
        return float(context[:-1]) * 1000
    
    elif context.endswith("K"): 
        return float(context[:-1])
    
    raise ValueError(f"Unknown context: {context}")

def normalize_feature(data, key):
    values = [d[key] for d in data]

    minimum = min(values)
    maximum = max(values)

    for d in data:
        d[key + "_normalized"] = (
            (d[key] - minimum)
            /
            (maximum - minimum)
        )


def normalize_data(data):

    for d in data:
        d['parameter'] = normalize_variants(d['variant'])
        d['context'] = normalize_context(d['context'])
        d['storage'] = normalize_storage(d['storage'])
    
    normalize_feature(data, 'parameter')
    normalize_feature(data, 'context')

    return data