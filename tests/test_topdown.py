import unittest
from unittest.mock import patch
from app import app


class TestTopDownIntegration(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    @patch("app.validate_input")
    @patch("app.convert_temperature")
    @patch("app.add_to_history")
    def test_app_only_with_stubs(self, mock_history, mock_convert, mock_validate):
        """TC-01: Menguji modul app.py secara terisolasi menggunakan stubs penuh"""
        mock_validate.return_value = 100.0
        mock_convert.return_value = 212.0

        response = self.client.post("/", data={
            "value": "100",
            "from_unit": "Celsius",
            "to_unit": "Fahrenheit"
        })

        mock_validate.assert_called_once_with("100", "Celsius", "Fahrenheit")
        mock_convert.assert_called_once_with(100.0, "Celsius", "Fahrenheit")
        mock_history.assert_called_once_with(100.0, "Celsius", 212.0, "Fahrenheit")
        self.assertIn(b"100.0 Celsius = 212.0 Fahrenheit", response.data)

    @patch("app.convert_temperature")
    @patch("app.add_to_history")
    def test_app_and_validator_integration(self, mock_history, mock_convert):
        """TC-02 & TC-03: Menguji integrasi app.py dengan validators.py asli (Logika bawah di-stub)"""
        mock_convert.return_value = 122.0

        # Kasus input Kelvin Negatif (Skenario Eror)
        response_error = self.client.post("/", data={
            "value": "-10",
            "from_unit": "Kelvin",
            "to_unit": "Celsius"
        })
        self.assertIn(b"Kelvin tidak boleh bernilai negatif", response_error.data)
        mock_convert.assert_not_called()
        mock_history.assert_not_called()

        # Kasus input Normal
        response_valid = self.client.post("/", data={
            "value": "50",
            "from_unit": "Celsius",
            "to_unit": "Fahrenheit"
        })
        self.assertIn(b"50.0 Celsius = 122.0 Fahrenheit", response_valid.data)


if __name__ == "__main__":
    unittest.main()