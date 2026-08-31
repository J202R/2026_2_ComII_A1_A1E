import numpy as np
from gnuradio import gr

class psd_autocorr(gr.sync_block):
    """PSD estimada vía autocorrelación (Wiener-Khinchin)"""

    def __init__(self, N=1024, max_lag=256):
        gr.sync_block.__init__(self,
            name='PSD',
            in_sig=[np.float32],
            out_sig=[np.float32])
        self.N = N
        self.max_lag = max_lag

    def work(self, input_items, output_items):
        x = input_items[0][:self.N]
        if len(x) < self.N:
            return 0  # esperar a tener suficientes muestras

        # --- Autocorrelación (equivalente a tu acumulador, pero
        #     sumando x[n]*x[n+lag] en vez de x[n]) ---
        # np.correlate ya vectoriza la suma que haría tu bloque acumulador
        full = np.correlate(x, x, mode='full')
        mid = len(full) // 2
        Rxx = full[mid: mid + self.max_lag] / self.N

        # Ventaneo opcional (reduce fuga espectral)
        Rxx *= np.hanning(self.max_lag)

        # --- PSD = FFT de la autocorrelación ---
        psd = np.abs(np.fft.fft(Rxx))
        psd_db = 10 * np.log10(psd + 1e-12)

        n_out = min(len(output_items[0]), len(psd_db))
        output_items[0][:n_out] = psd_db[:n_out]
        return n_out
