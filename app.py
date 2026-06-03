from flask import Flask, render_template, request
from converter import convert_temperature
from validators import validate_input
from history import add_to_history, get_history

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        value = request.form.get("value")
        from_unit = request.form.get("from_unit")
        to_unit = request.form.get("to_unit")

        try:
            validated_value = validate_input(value, from_unit, to_unit)
            converted_value = convert_temperature(validated_value, from_unit, to_unit)
            result = f"{validated_value} {from_unit} = {converted_value} {to_unit}"
            
            # Integrasi: Menyimpan ke riwayat jika seluruh proses di atas sukses
            add_to_history(validated_value, from_unit, converted_value, to_unit)
        except ValueError as e:
            error = str(e)

    # Mengambil data riwayat terbaru untuk dirender ke halaman web
    history_data = get_history()
    return render_template("index.html", result=result, error=error, history=history_data)


if __name__ == "__main__":
    app.run(debug=True)