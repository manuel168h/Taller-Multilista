import os
from flask import Flask, jsonify, render_template
from multilista import cargar_divipola_desde_csv

app = Flask(__name__)

# Definir la ruta absoluta basada en la ubicación de este archivo app.py
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "DIVIPOLA-_C_digos_municipios_20250505.csv")

# Cargar la multilista usando la ruta segura
multilista_colombia = cargar_divipola_desde_csv(csv_path)

@app.route('/api/divipola', methods=['GET'])
def obtener_divipola_json():
    return jsonify(multilista_colombia.to_dict())

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)