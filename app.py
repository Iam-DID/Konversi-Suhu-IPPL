from flask import Flask, render_template, request
from converter import convert_temperature
from validators import validate_input

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
        except ValueError as e:
            error = str(e)

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)