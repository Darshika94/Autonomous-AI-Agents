cache = {}

def cache_flag(txn_id, reason):
    cache[txn_id] = reason

def get_cached(txn_id):
    return cache.get(txn_id)
