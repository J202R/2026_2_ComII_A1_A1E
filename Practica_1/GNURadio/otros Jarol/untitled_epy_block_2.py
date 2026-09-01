import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='Promedios_de_tiempos',
            in_sig=[np.float32],
            out_sig=[np.float32, np.float32, np.float32, np.float32, np.float32]
        )
        # Variables de estado persistentes
        self.acum_x = 0.0
        self.acum_x2 = 0.0
        self.Ntotales = 0

    def work(self, input_items, output_items):
        x = input_items[0]       # Señal de entrada
        y0 = output_items[0]     # Promedio acumulado (Media)
        y1 = output_items[1]     # Media cuadrática (MS)
        y2 = output_items[2]     # RMS
        y3 = output_items[3]     # Potencia promedio
        y4 = output_items[4]     # Desviación estándar (Std)
        
        N = len(x)
        if N == 0:
            return 0
            
        # 1. Actualizar el contador global de muestras
        self.Ntotales += N
        
        # 2. Acumulación histórica lineal y cuadrática
        self.acum_x += np.sum(x)
        self.acum_x2 += np.sum(x**2)
        
        # 3. Cálculo de estimadores temporales globales
        media_global = self.acum_x / self.Ntotales
        ms_global = self.acum_x2 / self.Ntotales      # Media de los cuadrados
        rms_global = np.sqrt(ms_global)
        
        # 4. Varianza = E[X^2] - (E[X])^2
        varianza = ms_global - (media_global**2)
        if varianza < 0: 
            varianza = 0  # Evita errores numéricos de precisión por flotantes
        std_global = np.sqrt(varianza)
        
        # 5. Asignar los valores calculados a los vectores de salida de GRC
        y0[:] = media_global
        y1[:] = ms_global
        y2[:] = rms_global
        y3[:] = ms_global  # En ingeniería, la potencia promedio de una señal es su MS
        y4[:] = std_global
        
        return len(x)

