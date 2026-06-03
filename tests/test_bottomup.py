import unittest
from converter import convert_temperature
from validators import validate_input
from history import add_to_history, get_history, clear_history
from app import app


class TestBottomUpIntegration(unittest.TestCase):

    def setUp(self):
        clear_history()

    def test_converter_logic_only(self):
        """TC-07: Menguji keakuratan modul logika tingkat paling bawah secara mandiri"""
        self.assertEqual(convert_temperature(100, "Celsius", "Fahrenheit"), 212.0)
        self.assertEqual(convert_temperature(0, "Celsius", "Kelvin"), 273.15)

    def test_history_fifo_limit(self):
        """TC-11: Menguji aturan batas penampungan FIFO pada modul history"""
        for i in range(6):
            add_to_history(i, "Celsius", i * 2, "Fahrenheit")
        
        current_history = get_history()
        self.assertEqual(len(current_history), 5)
        self.assertIn("1.0 Celsius = 2.0 Fahrenheit", current_history[0])
        self.assertNotIn("0.0 Celsius = 0.0 Fahrenheit", current_history)

    def test_full_bottom_up_integration(self):
        """TC-10: Menguji seluruh subsistem terintegrasi penuh dari bawah ke atas menggunakan Driver Flask"""
        client = app.test_client()

        response = client.post("/", data={
            "value": "10",
            "from_unit": "Celsius",
            "to_unit": "Reamur"
        })
        
        # Memastikan output teks ter-render di antarmuka web
        self.assertIn(b"10.0 Celsius = 8.0 Reamur", response.data)
        
        # Memastikan data otomatis mengalir dan tersimpan ke komponen modul history
        self.assertEqual(len(get_history()), 1)
        self.assertEqual(get_history()[0], "10.0 Celsius = 8.0 Reamur")


if __name__ == "__main__":
    unittest.main()