import numpy as np
from gnuradio import gr

class blk(gr.sync_block):

    def __init__(self):  
        gr.sync_block.__init__(
            self,
            name='e_Diff',   
            in_sig=[np.float32],
            out_sig=[np.float32]
        ) # <-- El paréntesis de cierre va aquí

        # Memoria para guardar la última muestra del bloque de datos anterior
        self.muestra_anterior = 0.0

    def work(self, input_items, output_items):
        x = input_items[0]   # Señal de entrada
        y0 = output_items[0] # Señal de salida diferencial
        
        if len(x) == 0:
            return 0

        # Para derivar, insertamos la última muestra del paquete anterior al inicio
        x_completo = np.insert(x, 0, self.muestra_anterior)
        
        # np.diff calcula la diferencia entre elementos adyacentes: x[n] - x[n-1]
        y0[:] = np.diff(x_completo)
        
        # Guardamos la última muestra actual para usarla en el siguiente ciclo
        self.muestra_anterior = x[-1]
        
        return len(y0) # <-- Corregido: len(y0)