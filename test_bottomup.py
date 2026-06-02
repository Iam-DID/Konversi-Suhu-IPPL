import unittest
from converter import convert_temperature
from validators import validate_input
from app import app

class TestBottomUpIntegration(unittest.TestCase):
    
    def test_converter_logic_only(self):
        self.assertEqual(convert_temperature(100, 'Celsius', 'Fahrenheit'), 212.0)
        self.assertEqual(convert_temperature(0, 'Celsius', 'Kelvin'), 273.15)
        self.assertEqual(convert_temperature(80, 'Reamur', 'Celsius'), 100.0)

    def test_validator_and_converter_integration(self):
        raw_value = "40"
        from_unit = "Celsius"
        to_unit = "Reamur"

        validated_val = validate_input(raw_value, from_unit, to_unit)
        self.assertEqual(validated_val, 40.0)

        result = convert_temperature(validated_val, from_unit, to_unit)
        self.assertEqual(result, 32.0)

    def test_full_bottom_up_integration(self):
        client = app.test_client()
        
        response = client.post('/', data={
            'value': '10',
            'from_unit': 'Celsius',
            'to_unit': 'Reamur'
        })
        self.assertIn(b'10.0 Celsius = 8.0 Reamur', response.data)

        response_invalid = client.post('/', data={
            'value': 'abc',
            'from_unit': 'Celsius',
            'to_unit': 'Fahrenheit'
        })
        self.assertIn(b'Nilai suhu harus berupa angka', response_invalid.data)

if __name__ == '__main__':
    unittest.main()