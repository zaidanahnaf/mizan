import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FuzzyImpulsivePredictor:
    def __init__(self):
        """Mendefinisikan dan membangun sistem inferensi fuzzy."""
        # 1. Definisikan Variabel Input (Antecedents) sesuai form
        # Input Rasio: Seberapa besar pengeluaran dibanding budget. Rasio 1.0 = pas. > 1.0 = boros.
        self.rasio = ctrl.Antecedent(np.arange(0, 3.1, 0.1), 'rasio_pengeluaran')
        # Input Frekuensi: Seberapa sering belanja dalam sebulan.
        self.frekuensi = ctrl.Antecedent(np.arange(1, 11, 1), 'frekuensi')
        # Input Kategori: 0 untuk Primer, 1 untuk Tersier.
        self.kategori = ctrl.Antecedent(np.arange(0, 2, 1), 'kategori')

        # 2. Definisikan Variabel Output (Consequent)
        # Tingkat Impulsif dengan skala 0-100.
        self.impulsif = ctrl.Consequent(np.arange(0, 101, 1), 'tingkat_impulsif')

        # 3. Definisikan Fungsi Keanggotaan (Membership Functions)
        self._define_memberships()

        # 4. Definisikan Aturan (Rules)
        rules = self._define_rules()

        # 5. Bangun Sistem Kontrol
        self.control_system = ctrl.ControlSystem(rules)
        self.simulation = ctrl.ControlSystemSimulation(self.control_system)

    def _define_memberships(self):
        """Mendefinisikan bentuk-bentuk kurva fuzzy untuk setiap variabel."""
        # Rasio: 'hemat' (di bawah budget), 'boros' (sedikit di atas), 'sangat_boros' (jauh di atas)
        self.rasio['hemat'] = fuzz.trimf(self.rasio.universe, [0, 0, 1])
        self.rasio['boros'] = fuzz.trimf(self.rasio.universe, [0.8, 1.5, 2.2])
        self.rasio['sangat_boros'] = fuzz.trapmf(self.rasio.universe, [2, 2.5, 3, 3])

        # Frekuensi: 'jarang', 'sedang', 'sering'
        self.frekuensi['jarang'] = fuzz.trimf(self.frekuensi.universe, [1, 1, 4])
        self.frekuensi['sedang'] = fuzz.trimf(self.frekuensi.universe, [3, 5, 8])
        self.frekuensi['sering'] = fuzz.trimf(self.frekuensi.universe, [7, 10, 10])

        # Kategori: Biner, 'primer' (di 0) dan 'tersier' (di 1)
        self.kategori['primer'] = fuzz.trimf(self.kategori.universe, [0, 0, 0])
        self.kategori['tersier'] = fuzz.trimf(self.kategori.universe, [1, 1, 1])

        # Output Impulsif: 'tidak', 'cukup', 'sangat'
        self.impulsif['tidak'] = fuzz.trimf(self.impulsif.universe, [0, 20, 40])
        self.impulsif['cukup'] = fuzz.trimf(self.impulsif.universe, [30, 50, 70])
        self.impulsif['sangat'] = fuzz.trimf(self.impulsif.universe, [60, 80, 100])

    def _define_rules(self):
        """Membuat aturan-aturan fuzzy yang logis berdasarkan input yang baru."""
        # Pola umum: Rasio tinggi, frekuensi sering, dan kategori tersier meningkatkan impulsivitas.
        rule1 = ctrl.Rule(self.rasio['hemat'] & self.kategori['primer'] & self.frekuensi['jarang'], self.impulsif['tidak'])
        rule2 = ctrl.Rule(self.rasio['hemat'] & self.kategori['primer'], self.impulsif['tidak'])
        
        rule3 = ctrl.Rule(self.rasio['boros'] & self.kategori['primer'], self.impulsif['cukup'])
        rule4 = ctrl.Rule(self.frekuensi['sedang'] & self.rasio['hemat'], self.impulsif['cukup'])  
        
        rule5 = ctrl.Rule(self.rasio['sangat_boros'] & self.kategori['tersier'], self.impulsif['sangat'])
        rule6 = ctrl.Rule(self.rasio['boros'] & self.frekuensi['sering'], self.impulsif['sangat'])
        rule7 = ctrl.Rule(self.kategori['tersier'] & self.frekuensi['sering'], self.impulsif['sangat'])
        rule8 = ctrl.Rule(self.frekuensi['sedang'] & self.rasio['boros'], self.impulsif['sangat'])
        rule9 = ctrl.Rule(self.rasio['boros'] & self.kategori['tersier'], self.impulsif['sangat'])
        rule10 = ctrl.Rule(self.rasio['sangat_boros'] & self.kategori['primer'], self.impulsif['sangat'])
        rule11 = ctrl.Rule(self.frekuensi['jarang'] & self.kategori['tersier'] & self.rasio['sangat_boros'], self.impulsif['sangat'])

        return [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11] 

    def predict(self, rasio_value, frekuensi_value, kategori_value):
        """Melakukan prediksi berdasarkan input yang sudah diproses."""
        try:
            self.simulation.input['rasio_pengeluaran'] = rasio_value
            self.simulation.input['frekuensi'] = frekuensi_value
            self.simulation.input['kategori'] = kategori_value

            self.simulation.compute()
            
            score = self.simulation.output['tingkat_impulsif']
            
            # Klasifikasi hasil skor ke dalam 3 level
            if score <= 40:
                level = 0
                label = "Tidak Impulsif"
            elif score <= 70:
                level = 1
                label = "Cukup Impulsif"
            else:
                level = 2
                label = "Sangat Impulsif"

            return {
                "status": "success",
                "impulsive_score": round(score, 2),
                "impulsive_level": level,
                "impulsive_label": label
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}