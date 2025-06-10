import base64
import io
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from fuzzy_system import FuzzyImpulsivePredictor
from visualization import visualize_membership_functions
from evaluator import FuzzyClassifierEvaluator

app = Flask(__name__)
CORS(app)

# Inisialisasi komponen utama aplikasi
try:
    predictor = FuzzyImpulsivePredictor()
    evaluator = FuzzyClassifierEvaluator()
    # Muat dataset untuk evaluasi
    dataset = pd.read_csv('budget.csv')
except Exception as e:
    print(f"FATAL: Gagal menginisialisasi aplikasi. Error: {e}")
    predictor = None
    evaluator = None
    dataset = None

# Variabel global untuk menyimpan data input terakhir dari prediksi
last_prediction_input = None

@app.route('/')
def index():
    """Menyajikan halaman HTML utama."""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict_api():
    """API endpoint untuk membuat satu prediksi impulsivitas."""
    global last_prediction_input
    if not predictor:
        return jsonify({"error": "Sistem prediksi tidak terinisialisasi."}), 500

    try:
        data = request.get_json()
        
        # Validasi input
        budget_ideal = float(data['budgetIdeal'])
        pengeluaran_aktual = float(data['pengeluaranAktual'])
        frekuensi = int(data['frekuensi'])
        kategori_str = data['kategori']

        if budget_ideal <= 0:
            return jsonify({"error": "Budget ideal harus lebih dari 0"}), 400

        # Pre-processing: Ubah input mentah menjadi input untuk sistem fuzzy
        rasio = pengeluaran_aktual / budget_ideal
        kategori_numeric = 1 if kategori_str == 'tersier' else 0

        # Simpan input yang sudah diproses untuk visualisasi nanti
        last_prediction_input = {
            'rasio_pengeluaran': rasio,
            'frekuensi': frekuensi,
            'kategori': kategori_numeric
        }
        
        # Panggil sistem fuzzy untuk prediksi
        result = predictor.predict(rasio, frekuensi, kategori_numeric)
        
        return jsonify(result)

    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": f"Input tidak valid atau hilang: {e}"}), 400
    except Exception as e:
        return jsonify({"error": f"Terjadi kesalahan internal: {e}"}), 500

@app.route('/api/visualize_memberships', methods=['POST'])
def visualize_api():
    """API endpoint untuk membuat visualisasi fungsi keanggotaan."""
    if not predictor:
        return jsonify({"error": "Sistem prediksi tidak terinisialisasi."}), 500
        
    data = request.get_json()
    input_values = data.get('inputs') # Menerima input dari frontend

    try:
        img_bytes = visualize_membership_functions(predictor, input_values)
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        return jsonify({"plot_url": img_base64})
    except Exception as e:
        return jsonify({"error": f"Gagal membuat visualisasi: {e}"}), 500

@app.route('/api/evaluate_model', methods=['GET'])
def evaluate_api():
    """API endpoint untuk mengevaluasi model menggunakan dataset budget.csv."""
    if not predictor or not evaluator or dataset is None:
        return jsonify({"error": "Sistem evaluasi atau dataset tidak tersedia."}), 500

    try:
        evaluator.reset_data() # Pastikan data evaluasi kosong sebelum run baru

        # Mapping label string ke numerik
        label_map = {"Tidak Impulsif": 0, "Cukup Impulsif": 1, "Sangat Impulsif": 2}

        for _, row in dataset.iterrows():
            # Pre-processing data dari CSV
            rasio = row['pengeluaran(jt)/Bulan'] / row['Budget(jt)/Bulan']
            frekuensi = row['frekuensi']
            kategori_numeric = 1 if row['jenis_barang'] == 'Tersier' else 0
            actual_label = label_map.get(row['label'], -1)

            if actual_label == -1: continue # Lewati jika label tidak valid

            # Dapatkan prediksi dari model
            result = predictor.predict(rasio, frekuensi, kategori_numeric)
            
            # Tambahkan ke evaluator
            evaluator.add_evaluation(
                predicted=result['impulsive_level'],
                actual=actual_label,
                fuzzy_output=result['impulsive_score'],
                inputs={'rasio': rasio, 'frekuensi': frekuensi, 'kategori': kategori_numeric}
            )

        # Hitung metrik dan buat visualisasi performa
        metrics = evaluator.calculate_metrics()
        plot_bytes = evaluator.visualize_performance_to_bytes()
        plot_base64 = base64.b64encode(plot_bytes).decode('utf-8')

        return jsonify({
            "metrics": metrics,
            "plot_url": plot_base64
        })
    except Exception as e:
        return jsonify({"error": f"Gagal melakukan evaluasi: {e}"}), 500

if __name__ == '__main__':
    print("Starting Flask application on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)