import sys

sys.path.append("midasLib")
sys.path.append("bengalaFecaf/midasLib")

import run

class Midas:
    def __init__(self):
        self.modelo = "midas_v21_small_256.pt"
        self.tipo_modelo = "midas_v21_small_256"
        self._model = None
        self.transform = None
        self.net_w = None
        self.net_h = None
    
    def carregar(self):
        self._model, self.transform, self.net_w, self.net_h, = run.preload(
            "bengalaFecaf/weights/"+self.modelo,
            self.tipo_modelo,
            False,
            None,
            False)
        return None
    
    def avaliar(self, imagem):
        run.run_with_model(self._model, self.transform, self.net_w, self.net_h, imagem, "images/runs_midas", model_type=self.tipo_modelo, optimize=False, side=False, grayscale=True)
        return None