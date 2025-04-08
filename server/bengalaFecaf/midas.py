import sys
import os

sys.path.append("midasLib")
sys.path.append("bengalaFecaf/midasLib")

import run
from contextlib import contextmanager

@contextmanager
def ocultar_prints():
    stdout_original = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    try:
        yield
    finally:
        sys.stdout.close()
        sys.stdout = stdout_original

class Midas:
    def __init__(self):
        self.modelo = "midas_v21_small_256.pt"
        self.tipo_modelo = "midas_v21_small_256"
        self._model = None
        self.transform = None
        self.net_w = None
        self.net_h = None
    
    def carregar(self):
        with ocultar_prints():
            self._model, self.transform, self.net_w, self.net_h, = run.preload(
                "bengalaFecaf/weights/"+self.modelo,
                self.tipo_modelo,
                False,
                64,
                False)
        return None
    
    def avaliar(self, imagem):
        with ocultar_prints():
            run.run_with_model(self._model, self.transform, self.net_w, self.net_h, imagem, "images/runs_midas", model_type=self.tipo_modelo, optimize=True, side=False, grayscale=True)
        return None