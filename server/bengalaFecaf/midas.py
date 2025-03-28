import sys

sys.path.append("midasLib")
sys.path.append("bengalaFecaf/midasLib")

import run

class Midas:
    def __init__(self):
        self.modelo = "dpt_large_384.pt"
        self.tipo_modelo = "dpt_large_384.pt"
        self.qualidade = 384
        self.model = None
        self.transform = None
        self.net_w = None
        self.net_h = None

    def treinar(self):
        return None
    
    def carregar(self):
        self.model, self.transform, self.net_w, self.net_h, = run.preload(
            "bengalaFecaf/weights/dpt_large_384.pt",
            "dpt_large_384",
            False,
            None,
            False)
        return None
    
    def avaliar(self):

        run.run_with_model(self.model, self.transform, self.net_w, self.net_h, "images/photos", "images/runs_midas", model_type=self.tipo_modelo, optimize=False, side=False, grayscale=True)
        return None