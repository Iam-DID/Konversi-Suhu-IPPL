_history_list = []


def add_to_history(value, from_unit, result, to_unit):
    """Menambahkan riwayat konversi dengan aturan FIFO (Maksimal 5 data terbaru)"""
    entry = f"{value} {from_unit} = {result} {to_unit}"
    _history_list.append(entry)
    
    if len(_history_list) > 5:
        _history_list.pop(0)
    return entry


def get_history():
    """Mengambil semua daftar riwayat saat ini"""
    return _history_list


def clear_history():
    """Mengosongkan semua daftar riwayat"""
    global _history_list
    _history_list = []