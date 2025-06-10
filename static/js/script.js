document.addEventListener('DOMContentLoaded', () => {
    // --- Bagian 1: Deklarasi semua elemen DOM ---
    const form = document.getElementById('impulsiveForm');
    const submitBtn = document.getElementById('submitBtn');
    const resultSection = document.getElementById('resultSection');
    const resultBadge = document.getElementById('resultBadge');
    const resultText = document.getElementById('resultText');
    const showDetailBtn = document.getElementById('showDetailBtn');
    const saveBtn = document.getElementById('saveBtn');
    const resetBtn = document.getElementById('resetBtn');
    const historyContent = document.getElementById('historyContent');
    const evaluateModelBtn = document.getElementById('evaluateModelBtn');
    const evaluationResultContainer = document.getElementById('evaluationResultContainer');
    const categoryOptions = document.querySelectorAll('.category-option');
    const modal = document.getElementById('plotModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    const modalCloseBtn = document.querySelector('.modal-close-btn');
    const historyAnalysisBtn = document.getElementById('historyAnalysisBtn');
    const historyAnalysisDashboard = document.getElementById('historyAnalysisDashboard');
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');

    // --- Bagian 2: State Management ---
    let transactions = JSON.parse(localStorage.getItem('transactions')) || [];
    let currentResult = null;
    let lastInputsForViz = null;

    // --- Bagian 3: Deklarasi semua fungsi ---

    const updateHistoryTable = () => {
        if (transactions.length === 0) {
            historyContent.innerHTML = `<div class="empty-state"><p>Belum ada transaksi yang disimpan.</p></div>`;
            historyAnalysisBtn.style.display = 'none';
            clearHistoryBtn.style.display = 'none';
            return;
        }
        historyAnalysisBtn.style.display = 'inline-flex';
        clearHistoryBtn.style.display = 'inline-flex';
        
        const labelToClassMap = {'Tidak Impulsif': 'tidak-impulsif', 'Cukup Impulsif': 'cukup-impulsif', 'Sangat Impulsif': 'sangat-impulsif' };
        
        const tableRows = transactions.map(t => {
            const labelClass = labelToClassMap[t.result.impulsive_label] || '';
            return `
                <tr>
                    <td>${t.keperluan}</td>
                    <td>Rp${(parseFloat(t.budgetIdeal) * 1000000).toLocaleString('id-ID')}</td>
                    <td>Rp${(parseFloat(t.pengeluaranAktual) * 1000000).toLocaleString('id-ID')}</td>
                    <td>${t.frekuensi}x</td>
                    <td style="text-transform: capitalize;">${t.kategori}</td>
                    <td><span class="history-label ${labelClass}">${t.result.impulsive_label}</span></td>
                    <td>${new Date(t.timestamp).toLocaleDateString('id-ID')}</td>
                </tr>`;
        }).join('');
        historyContent.innerHTML = `<table class="history-table"><thead><tr><th>Keperluan</th><th>Budget</th><th>Aktual</th><th>Frekuensi</th><th>Kategori</th><th>Hasil Analisis</th><th>Tanggal</th></tr></thead><tbody>${tableRows}</tbody></table>`;
    };

    const displayPredictionResult = (data, formData) => {
        const { impulsive_label, impulsive_level } = data;
        const messages = { 0: "Luar biasa! Pengeluaran ini sangat bijak dan terkontrol. Pertahankan!", 1: "Cukup impulsif. Ada ruang untuk perbaikan. Coba pikirkan kembali sebelum membeli lain kali.", 2: "Sangat impulsif! Ini adalah tanda bahaya. Waspadai pengeluaran seperti ini di masa depan." };
        const icons = { 0: '✅', 1: '⚠️', 2: '🚨' };
        const badgeClasses = { 0: 'tidak-impulsif', 1: 'cukup-impulsif', 2: 'sangat-impulsif' };
        
        resultBadge.className = `result-badge ${badgeClasses[impulsive_level]}`;
        resultBadge.innerHTML = `${icons[impulsive_level] || ''} ${impulsive_label}`;
        resultText.textContent = messages[impulsive_level];
        resultSection.style.display = 'block';
        currentResult = { ...formData, result: data, timestamp: new Date() };
    };

    const showLoadingState = (button, isLoading, originalText) => {
        if (isLoading) {
            button.disabled = true;
            button.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Memproses...`;
        } else {
            button.disabled = false;
            button.innerHTML = originalText;
        }
    };

    const showModal = (title, content) => {
        modalTitle.textContent = title;
        modalBody.innerHTML = content;
        modal.style.display = 'block';
    };

    const createFinancialDashboard = () => {
        if (transactions.length === 0) {
            historyAnalysisDashboard.innerHTML = `<div class="empty-state"><p>Tidak ada data untuk dianalisis. Silakan simpan beberapa transaksi terlebih dahulu.</p></div>`;
            historyAnalysisDashboard.style.display = 'block';
            return;
        }

        // 1. Hitung Metrik Finansial (KPIs) - Tidak ada perubahan di sini
        const totalSpending = transactions.reduce((sum, t) => sum + parseFloat(t.pengeluaranAktual), 0);
        const totalBudget = transactions.reduce((sum, t) => sum + parseFloat(t.budgetIdeal), 0);
        const spendingByCategory = transactions.reduce((acc, t) => {
            acc[t.kategori] = (acc[t.kategori] || 0) + parseFloat(t.pengeluaranAktual);
            return acc;
        }, {});
        const countByImpulsiveLevel = transactions.reduce((acc, t) => {
            acc[t.result.impulsive_label] = (acc[t.result.impulsive_label] || 0) + 1;
            return acc;
        }, {});

        // 2. Buat HTML untuk KPI Cards - Tidak ada perubahan di sini
        const kpiHTML = `
            <div class="kpi-grid">
                <div class="kpi-card"><div class="kpi-title">Total Pengeluaran</div><div class="kpi-value">Rp${(totalSpending * 1000000).toLocaleString('id-ID')}</div></div>
                <div class="kpi-card"><div class="kpi-title">Total Budget</div><div class="kpi-value">Rp${(totalBudget * 1000000).toLocaleString('id-ID')}</div></div>
                <div class="kpi-card"><div class="kpi-title">Pengeluaran Primer</div><div class="kpi-value">${spendingByCategory.primer ? 'Rp' + (spendingByCategory.primer * 1000000).toLocaleString('id-ID') : 'Rp0'}</div></div>
                <div class="kpi-card"><div class="kpi-title">Pengeluaran Tersier</div><div class="kpi-value">${spendingByCategory.tersier ? 'Rp' + (spendingByCategory.tersier * 1000000).toLocaleString('id-ID') : 'Rp0'}</div></div>
            </div>`;

        // 3. Buat Grafik - Logika Pie Chart Diperbaiki
        const primerAmount = spendingByCategory.primer || 0;
        const tersierAmount = spendingByCategory.tersier || 0;
        const totalForPie = primerAmount + tersierAmount;
        
        // Hitung persentase untuk conic-gradient
        const primerPercent = totalForPie > 0 ? (primerAmount / totalForPie) * 100 : 0;
        
        // <<< DIUBAH: Menggunakan div dengan background conic-gradient, jauh lebih andal
        const pieChartHTML = `
            <div style="width: 150px; height: 150px; border-radius: 50%; background: conic-gradient(#2E7D32 0% ${primerPercent}%, #FF9800 ${primerPercent}% 100%); margin: 0 auto;"></div>
            <div style="text-align:center; margin-top:1rem;">
                <span style="color:#2E7D32;">■</span> Primer (${primerPercent.toFixed(1)}%) &nbsp;
                <span style="color:#FF9800;">■</span> Tersier (${(100 - primerPercent).toFixed(1)}%)
            </div>
        `;

        // Bar Chart untuk Level Impulsif - Tidak ada perubahan di sini
        const counts = [countByImpulsiveLevel['Tidak Impulsif'] || 0, countByImpulsiveLevel['Cukup Impulsif'] || 0, countByImpulsiveLevel['Sangat Impulsif'] || 0];
        const maxCount = Math.max(...counts, 1);
        const barChartHTML = `<div style="display:flex; justify-content:space-around; align-items:flex-end; height:150px; border-left:2px solid #ccc; border-bottom:2px solid #ccc; padding-left:10px;"><div style="height:${(counts[0]/maxCount)*100}%; background-color:#2E7D32; width:25%;" title="Tidak Impulsif: ${counts[0]}"></div><div style="height:${(counts[1]/maxCount)*100}%; background-color:#F57C00; width:25%;" title="Cukup Impulsif: ${counts[1]}"></div><div style="height:${(counts[2]/maxCount)*100}%; background-color:#D32F2F; width:25%;" title="Sangat Impulsif: ${counts[2]}"></div></div><div style="text-align:center; margin-top:0.5rem; font-size:0.8rem; color:#6c757d;">Tdk | Cukup | Sangat</div>`;

        // 4. Gabungkan semua menjadi satu dasbor - Tidak ada perubahan di sini
        historyAnalysisDashboard.innerHTML = `${kpiHTML}<div class="chart-grid"><div class="chart-container"><h4>Distribusi Pengeluaran</h4>${pieChartHTML}</div><div class="chart-container"><h4>Distribusi Level Impulsif</h4>${barChartHTML}</div></div>`;
        historyAnalysisDashboard.style.display = 'block';
    };

    // --- Bagian 4: Pendaftaran semua Event Listener ---
    
    categoryOptions.forEach(option => {
        option.addEventListener('click', () => {
            categoryOptions.forEach(opt => opt.classList.remove('selected'));
            option.classList.add('selected');
        });
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const originalBtnText = submitBtn.innerHTML;
        showLoadingState(submitBtn, true);
        const selectedCategory = document.querySelector('.category-option.selected');
        if (!selectedCategory) {
            alert('Silakan pilih kategori keperluan.');
            showLoadingState(submitBtn, false, originalBtnText);
            return;
        }
        const formData = {
            keperluan: document.getElementById('keperluan').value,
            budgetIdeal: document.getElementById('budgetIdeal').value,
            pengeluaranAktual: document.getElementById('pengeluaranAktual').value,
            frekuensi: document.getElementById('frekuensi').value,
            kategori: selectedCategory.dataset.category
        };
        try {
            const response = await fetch('/api/predict', {
                method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(formData)
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error);
            displayPredictionResult(data, formData);
            const rasio = parseFloat(formData.pengeluaranAktual) / parseFloat(formData.budgetIdeal);
            lastInputsForViz = {
                rasio_pengeluaran: rasio, frekuensi: parseInt(formData.frekuensi),
                kategori: formData.kategori === 'tersier' ? 1 : 0
            };
        } catch (err) {
            alert(`Error: ${err.message}`);
        } finally {
            showLoadingState(submitBtn, false, originalBtnText);
        }
    });

    saveBtn.addEventListener('click', () => {
        if (currentResult) {
            transactions.push(currentResult);
            localStorage.setItem('transactions', JSON.stringify(transactions));
            updateHistoryTable();
            alert('Hasil analisis berhasil disimpan!');
        }
    });

    resetBtn.addEventListener('click', () => {
        form.reset();
        categoryOptions.forEach(opt => opt.classList.remove('selected'));
        resultSection.style.display = 'none';
        currentResult = null;
        lastInputsForViz = null;
    });

    showDetailBtn.addEventListener('click', async () => {
        if (!lastInputsForViz) return;
        const originalBtnText = showDetailBtn.innerHTML;
        showLoadingState(showDetailBtn, true);

        try {
            const response = await fetch('/api/visualize_memberships', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ inputs: lastInputsForViz })
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error);
            
            showModal('Visualisasi Fungsi Keanggotaan', `<img src="data:image/png;base64,${data.plot_url}" alt="Plot Fungsi Keanggotaan">`);

        } catch (err) {
            alert(`Error: ${err.message}`);
        } finally {
            showLoadingState(showDetailBtn, false, originalBtnText);
        }
    });

    evaluateModelBtn.addEventListener('click', async () => {
        const originalBtnText = evaluateModelBtn.innerHTML;
        showLoadingState(evaluateModelBtn, true);
        evaluationResultContainer.style.display = 'block';
        evaluationResultContainer.innerHTML = `<p>Mengevaluasi model dengan dataset... Ini mungkin memakan waktu beberapa saat.</p>`;
        try {
            const response = await fetch('/api/evaluate_model');
            const data = await response.json();
            if (!response.ok) throw new Error(data.error);
            const metrics = data.metrics;
            const metricsHTML = `<h4>Hasil Evaluasi Model</h4><pre>Akurasi: ${metrics.accuracy}%\nMAE (Rata-rata Error): ${metrics.mae} level\nTotal Data Uji: ${metrics.total_evaluations}</pre><img src="data:image/png;base64,${data.plot_url}" alt="Plot Evaluasi Model">`;
            evaluationResultContainer.innerHTML = metricsHTML;
        } catch (err) {
            evaluationResultContainer.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
        } finally {
            showLoadingState(evaluateModelBtn, false, originalBtnText);
        }
    });

    historyAnalysisBtn.addEventListener('click', () => {
        const isDisplayed = historyAnalysisDashboard.style.display === 'block';
        if (isDisplayed) {
            historyAnalysisDashboard.style.display = 'none';
        } else {
            createFinancialDashboard();
        }
    });

    clearHistoryBtn.addEventListener('click', () => {
        if (transactions.length === 0) return;
        const isConfirmed = confirm('Apakah Anda yakin ingin menghapus semua riwayat transaksi? Tindakan ini tidak dapat dibatalkan.');
        if (isConfirmed) {
            transactions = [];
            localStorage.removeItem('transactions');
            updateHistoryTable();
            historyAnalysisDashboard.style.display = 'none';
            alert('Riwayat transaksi telah berhasil dibersihkan.');
        }
    });

    modalCloseBtn.addEventListener('click', () => modal.style.display = 'none');
    window.addEventListener('click', (e) => {
        if (e.target == modal) modal.style.display = 'none';
    });

    // --- Bagian 5: Initial Load ---
    updateHistoryTable();
});