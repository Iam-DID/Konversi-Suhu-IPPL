def to_celsius(value, from_unit):
    if from_unit == "Celsius":
        return value
    elif from_unit == "Fahrenheit":
        return (value - 32) * 5 / 9
    elif from_unit == "Kelvin":
        return value - 273.15
    elif from_unit == "Reamur":
        return value * 5 / 4
    else:
        raise ValueError("Satuan asal tidak valid")


def from_celsius(value, to_unit):
    if to_unit == "Celsius":
        return value
    elif to_unit == "Fahrenheit":
        return (value * 9 / 5) + 32
    elif to_unit == "Kelvin":
        return value + 273.15
    elif to_unit == "Reamur":
        return value * 4 / 5
    else:
        raise ValueError("Satuan tujuan tidak valid")


def convert_temperature(value, from_unit, to_unit):
    celsius_value = to_celsius(value, from_unit)
    result = from_celsius(celsius_value, to_unit)
    return round(result, 2)