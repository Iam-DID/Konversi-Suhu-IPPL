import unittest
from converter import convert_temperature
from validators import validate_input
from history import add_to_history, get_history, clear_history
from app import app

class TestBottomUpIntegration(unittest.TestCase):

    def setUp(self):
        clear_history()
        self.client = app.test_client()

    # ==========================================
    # TC-06: Murni Converter (Low-Level)
    # ==========================================
    def test_tc06_converter_logic_only(self):
        self.assertEqual(convert_temperature(100, "Celsius", "Fahrenheit"), 212.0)
        self.assertEqual(convert_temperature(0, "Celsius", "Kelvin"), 273.15)

    # ==========================================
    # TC-07: Murni History FIFO (Mid-Level)
    # ==========================================
    def test_tc07_history_fifo_limit(self):
        for i in range(6):
            add_to_history(i, "Celsius", i * 2, "Fahrenheit")
        
        current_history = get_history()
        self.assertEqual(len(current_history), 5) # Pastikan tidak lebih dari 5
        self.assertNotIn("0 Celsius = 0 Fahrenheit", current_history) # Data pertama harus hilang

    # ==========================================
    # TC-08: Integrasi Validators -> Converter
    # ==========================================
    def test_tc08_validator_to_converter(self):
        # Aliran Horizontal: String mentah diubah ke Float lalu dihitung
        validated_val = validate_input("50.5", "Celsius", "Reamur")
        result = convert_temperature(validated_val, "Celsius", "Reamur")
        
        self.assertEqual(validated_val, 50.5)
        self.assertEqual(result, 40.4)

    # ==========================================
    # TC-09: Integrasi Converter -> History
    # ==========================================
    def test_tc09_converter_to_history(self):
        # Aliran Horizontal: Hasil konversi dilempar ke riwayat
        result = convert_temperature(40.0, "Reamur", "Celsius")
        entry = add_to_history(40.0, "Reamur", result, "Celsius")
        
        self.assertEqual(result, 50.0)
        self.assertEqual(entry, "40.0 Reamur = 50.0 Celsius")
        self.assertIn("40.0 Reamur = 50.0 Celsius", get_history())

    # ==========================================
    # TC-10: Integrasi Penuh Berhasil (Driver Flask)
    # ==========================================
    def test_tc10_full_integration_success(self):
        response = self.client.post("/", data={
            "value": "10",
            "from_unit": "Celsius",
            "to_unit": "Reamur"
        })
        
        # Pastikan dirender ke HTML
        self.assertIn(b"10.0 Celsius = 8.0 Reamur", response.data)
        # Pastikan masuk ke memori history.py
        self.assertEqual(len(get_history()), 1)
        self.assertEqual(get_history()[0], "10.0 Celsius = 8.0 Reamur")

    # ==========================================
    # TC-11: Integrasi Penuh Gagal (Driver Flask)
    # ==========================================
    def test_tc11_full_integration_fail(self):
        response = self.client.post("/", data={
            "value": "", # Sengaja dikosongkan
            "from_unit": "Celsius",
            "to_unit": "Kelvin"
        })
        
        # Validasi harus menolak dan histori tidak boleh bertambah (tetap 0)
        self.assertIn(b"Nilai suhu harus berupa angka", response.data)
        self.assertEqual(len(get_history()), 0)

if __name__ == "__main__":
    unittest.main()