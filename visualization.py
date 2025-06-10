import matplotlib
matplotlib.use('Agg')
import io
import matplotlib.pyplot as plt
import skfuzzy as fuzz

def visualize_membership_functions(fuzzy_system, input_values=None):
    """
    Membuat visualisasi fungsi keanggotaan untuk sistem fuzzy yang baru.
    
    Args:
        fuzzy_system: Instance dari FuzzyImpulsivePredictor yang sudah diinisialisasi.
        input_values (dict): Nilai input aktual untuk ditandai di grafik. 
                             Contoh: {'rasio_pengeluaran': 1.5, 'frekuensi': 5, 'kategori': 1}
    
    Returns:
        bytes: Gambar plot dalam format PNG.
    """
    plt.style.use('ggplot')
    fig, axs = plt.subplots(4, 1, figsize=(8, 12))

    # Ekstrak variabel dari sistem fuzzy
    variables = {
        'Rasio Pengeluaran': fuzzy_system.rasio,
        'Frekuensi (kali/bulan)': fuzzy_system.frekuensi,
        'Kategori': fuzzy_system.kategori,
        'Tingkat Impulsif (Output)': fuzzy_system.impulsif,
    }
    
    input_keys = ['rasio_pengeluaran', 'frekuensi', 'kategori']
    
    for ax, (title, var) in zip(axs, variables.items()):
        for term_name, term_mf in var.terms.items():
            ax.plot(var.universe, term_mf.mf, label=term_name)
        
        ax.set_title(title)
        ax.legend()
        ax.grid(True)
        
        # Tambahkan marker jika ada input values
        if input_values and var.label in input_keys:
            input_val = input_values.get(var.label)
            if input_val is not None:
                ax.axvline(x=input_val, color='purple', linestyle='--', alpha=0.9, label=f'Input: {input_val:.2f}')
                # Re-add legend to include the new line
                ax.legend()

    fig.tight_layout()
    
    # Simpan ke buffer memori
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    return buf.getvalue()