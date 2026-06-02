VALID_UNITS = ["Celsius", "Fahrenheit", "Kelvin", "Reamur"]


def validate_input(value, from_unit, to_unit):
    try:
        value = float(value)
    except ValueError:
        raise ValueError("Nilai suhu harus berupa angka")

    if from_unit not in VALID_UNITS:
        raise ValueError("Satuan asal tidak valid")

    if to_unit not in VALID_UNITS:
        raise ValueError("Satuan tujuan tidak valid")

    if from_unit == "Kelvin" and value < 0:
        raise ValueError("Kelvin tidak boleh bernilai negatif")

    return value