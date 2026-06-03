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
    def test_tc01_normal_conversion(self, mock_history, mock_convert, mock_validate):
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
    def test_tc02_non_numeric_input(self, mock_history, mock_convert):
        response = self.client.post("/", data={
            "value": "abc",
            "from_unit": "Celsius",
            "to_unit": "Fahrenheit"
        })
        
        self.assertIn(b"Nilai suhu harus berupa angka", response.data)
        mock_convert.assert_not_called()
        mock_history.assert_not_called()

    @patch("app.convert_temperature")
    @patch("app.add_to_history")
    def test_tc03_negative_kelvin(self, mock_history, mock_convert):
        response = self.client.post("/", data={
            "value": "-15",
            "from_unit": "Kelvin",
            "to_unit": "Celsius"
        })
        
        self.assertIn(b"Kelvin tidak boleh bernilai negatif", response.data)
        mock_convert.assert_not_called()

    @patch("app.validate_input")
    @patch("app.convert_temperature")
    def test_tc04_history_page_load(self, mock_convert, mock_validate):
        from history import add_to_history, clear_history
        clear_history()
        add_to_history(50.0, "Celsius", 122.0, "Fahrenheit")

        response = self.client.get("/")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"50.0 Celsius = 122.0 Fahrenheit", response.data)
        
        mock_validate.assert_not_called()
        mock_convert.assert_not_called()

    @patch("app.convert_temperature")
    @patch("app.add_to_history")
    def test_tc05_invalid_unit(self, mock_history, mock_convert):
        response = self.client.post("/", data={
            "value": "25",
            "from_unit": "Reamur_Salah",
            "to_unit": "Celsius"
        })
        
        self.assertIn(b"Satuan asal tidak valid", response.data)
        mock_convert.assert_not_called()

if __name__ == "__main__":
    unittest.main()