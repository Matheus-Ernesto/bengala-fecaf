import os
from ultralytics import YOLO
import torch

class Yolo:
    def __init__(self):
        self.modelo = "yolov5nu_treinado.pt"
        self.tipo_modelo = "yolov5nu_treinado"
        self._model = None

    def treinar(self, yaml, qualidade, fatoracao):
        _model = YOLO(os.path.join("bengalaFecaf","weights",self.modelo))

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Usando dispositivo: {device}")

        train_results = _model.train(
            data=yaml,
            epochs=fatoracao,
            imgsz=qualidade,
            device=device,
            project="bengalaFecaf/training",
            name="train"
        )

        metrics = _model.val()
        return None
    
    def carregar(self):
        self._model = YOLO(os.path.join("bengalaFecaf","weights", self.modelo))
        return None
    
    def avaliar(self):
        results = self._model(os.path.join("images","photos","output.jpg"))
        if results and len(results) > 0:
            results[0].save(filename=os.path.join("images","runs_yolo","output.jpg"))
        return None