import numpy as np
from gnuradio import gr

class blk(gr.sync_block):

    def __init__(self):    # Doble guion bajo
        gr.sync_block.__init__(
            self,
            name='e_Acum',    
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # Estado de memoria: guarda el último valor del bloque anterior
        self.valor_anterior = 0.0

    def work(self, input_items, output_items):
        x = input_items[0]    # Señal de entrada
        y0 = output_items[0]  # Señal de salida

        # Calculamos la suma acumulada y le sumamos el estado anterior
        y0[:] = self.valor_anterior + np.cumsum(x)
        
        # Guardamos el último valor de este bloque para usarlo en el siguiente
        if len(y0) > 0:
            self.valor_anterior = y0[-1]

        return len(y0)  # Retornamos len(y0) en lugar de len(y)