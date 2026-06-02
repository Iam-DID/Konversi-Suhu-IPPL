from converter import to_celsius, from_celsius, convert_temperature


def driver_test_to_celsius():
    result = to_celsius(212, "Fahrenheit")
    print("212 Fahrenheit ke Celsius =", result)


def driver_test_from_celsius():
    result = from_celsius(100, "Fahrenheit")
    print("100 Celsius ke Fahrenheit =", result)


def driver_test_convert_temperature():
    result = convert_temperature(100, "Celsius", "Fahrenheit")
    print("100 Celsius ke Fahrenheit =", result)


if __name__ == "__main__":
    driver_test_to_celsius()
    driver_test_from_celsius()
    driver_test_convert_temperature()