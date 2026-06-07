_history_list = []

def add_to_history(value, from_unit, result, to_unit):
    entry = f"{value} {from_unit} = {result} {to_unit}"
    _history_list.append(entry)
    
    if len(_history_list) > 10:
        _history_list.pop(0)
    return entry

def get_history():
    return _history_list

def clear_history():
    global _history_list
    _history_list = []