import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='e_Acum',       # Comillas simples estándar de Python
            in_sig=[np.float32],
            out_sig=[np.float32]
        )

    def work(self, input_items, output_items):
        x = input_items[0]       # Señal de entrada
        y0 = output_items[0]     # Señal de salida asignada
        
        # Lógica del acumulador utilizando la función de NumPy
        y0[:] = np.cumsum(x)
        
        return len(y0)           # Retorna la longitud del vector de salida corregido

