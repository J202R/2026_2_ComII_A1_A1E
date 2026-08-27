import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='e_Diff',       # Comillas estándar de Python
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # La inicialización de tus variables de estado va FUERA del bloque anterior
        self.acum_anterior = 0.0

    def work(self, input_items, output_items):
        x = input_items[0]       # Señal de entrada
        y0 = output_items[0]     # Señal acumulada diferencial
        N = len(x)
        
        # Lógica de acumulación considerando el estado del bloque anterior
        diff = np.cumsum(x) + self.acum_anterior
        self.acum_anterior = diff[N - 1]
        
        y0[:] = diff
        return len(y0)           # Retorna la longitud del vector correcto (y0)

