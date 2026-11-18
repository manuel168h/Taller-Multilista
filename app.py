from flask import Flask, jsonify, render_template
from multilista import cargar_divipola_desde_csv

app = Flask(__name__)

multilista_colombia = cargar_divipola_desde_csv("DIVIPOLA-_C_digos_municipios_20250505.csv")

@app.route('/api/divipola', methods=['GET'])
def obtener_divipola_json():
    return jsonify(multilista_colombia.to_dict())

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)