import matplotlib
matplotlib.use('Agg') 
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class FuzzyClassifierEvaluator:
    def __init__(self):
        self.evaluation_data = []

    def add_evaluation(self, predicted: int, actual: int, fuzzy_output: float, inputs: dict):
        """Menambahkan satu data hasil evaluasi."""
        evaluation = {
            'predicted': predicted,
            'actual': actual,
            'fuzzy_output': fuzzy_output,
            'absolute_error': abs(predicted - actual),
            'is_correct': predicted == actual,
            'inputs': inputs
        }
        self.evaluation_data.append(evaluation)

    def calculate_metrics(self) -> dict:
        """Menghitung semua metrik performa klasifikasi."""
        if not self.evaluation_data:
            return {}

        n = len(self.evaluation_data)
        accuracy = sum(d['is_correct'] for d in self.evaluation_data) / n * 100
        mae = sum(d['absolute_error'] for d in self.evaluation_data) / n

        error_dist = {0: 0, 1: 0, 2: 0}
        for item in self.evaluation_data:
            err = item['absolute_error']
            if err in error_dist:
                error_dist[err] += 1
        
        matrix = self._calculate_confusion_matrix()

        return {
            'accuracy': round(accuracy, 2),
            'mae': round(mae, 3), # Mean Absolute Error (rata-rata salah berapa level)
            'total_evaluations': n,
            'error_distribution': error_dist,
            'confusion_matrix': matrix
        }

    def _calculate_confusion_matrix(self) -> list:
        """Menghitung confusion matrix dalam format list 2D untuk heatmap."""
        classes = [0, 1, 2] # 0:Tidak, 1:Cukup, 2:Sangat
        matrix = [[0 for _ in classes] for _ in classes]
        for item in self.evaluation_data:
            try:
                matrix[item['actual']][item['predicted']] += 1
            except IndexError:
                print(f"Warning: Invalid class label detected. Actual: {item['actual']}, Predicted: {item['predicted']}")
        return matrix

    def visualize_performance_to_bytes(self) -> bytes:
        """Membuat visualisasi performa dan mengembalikannya sebagai bytes PNG."""
        if not self.evaluation_data:
            raise ValueError("No data to visualize.")

        metrics = self.calculate_metrics()
        
        plt.style.use('ggplot')
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle('Hasil Evaluasi Performa Model Fuzzy', fontsize=16)

        # Plot 1: Confusion Matrix
        cm = metrics['confusion_matrix']
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0],
                    xticklabels=['Tidak', 'Cukup', 'Sangat'],
                    yticklabels=['Tidak', 'Cukup', 'Sangat'])
        axes[0].set_title('Confusion Matrix')
        axes[0].set_xlabel('Prediksi Model')
        axes[0].set_ylabel('Label Sebenarnya')

        # Plot 2: Distribusi Error
        error_dist = metrics['error_distribution']
        axes[1].bar(error_dist.keys(), error_dist.values(), color=['#2E7D32', '#F59E0B', '#D32F2F'])
        axes[1].set_title('Distribusi Error Prediksi')
        axes[1].set_xlabel('Besaran Error (Beda Level)')
        axes[1].set_ylabel('Jumlah Prediksi')
        axes[1].set_xticks([0, 1, 2])

        fig.tight_layout(rect=[0, 0, 1, 0.95])

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        return buf.getvalue()

    def reset_data(self):
        """Mereset data evaluasi."""
        self.evaluation_data = []