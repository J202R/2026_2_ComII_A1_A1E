import numpy as np
from gnuradio import gr

class blk(gr.decim_block):   # <-- CORRECCIÓN: era gr.sync_decimator
    def __init__(self, M=64):
        gr.decim_block.__init__(   # <-- también aquí
            self,
            name='Promedios_de_tiempos',
            in_sig=[np.float32],
            out_sig=[np.float32],
            decim=M
        )
        self.M = M

    def work(self, input_items, output_items):
        x = input_items[0]
        y0 = output_items[0]
        n_out = len(y0)

        for i in range(n_out):
            acum_x = 0.0
            Ntotales = 0

            ventana = x[i*self.M : (i+1)*self.M]

            Ntotales += len(ventana)
            acum_x += np.sum(ventana)

            media = acum_x / Ntotales
            y0[i] = media

        return n_out
