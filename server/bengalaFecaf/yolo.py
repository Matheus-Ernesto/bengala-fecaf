import os
from ultralytics import YOLO
import torch
import sys
import gc

import logging
logging.getLogger("ultralytics").setLevel(logging.CRITICAL)

from contextlib import contextmanager

@contextmanager
def ocultar_prints():
    stdout_original = sys.stdout
    stderr_original = sys.stderr
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    try:
        yield
    finally:
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = stdout_original
        sys.stderr = stderr_original


class Yolo:
    def __init__(self):
        self.modelo = "yolov5nu.pt"
        self._model = None

    def treinar(self, yaml, qualidade, fatoracao):
        self._model = YOLO(os.path.join("bengalaFecaf","weights",self.modelo))

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Usando dispositivo: {device}")

        train_results = self._model.train(
            data=yaml,
            epochs=fatoracao,
            imgsz=qualidade,
            device=device,
            project="bengalaFecaf/training",
            name="train"
        )

        metrics = self._model.val()

        return None
    
    def carregar(self):
        with ocultar_prints():
            self._model = YOLO(os.path.join("bengalaFecaf","weights", self.modelo))
        return None
    
    def avaliar(self, image): 
        with ocultar_prints():
            try:
                results = self._model(image)

                os.makedirs("images/runs_yolo", exist_ok=True)

                if results and len(results) > 0:
                    results[0].save(filename=os.path.join("images", "runs_yolo", "output.jpg"))

                del results
                gc.collect()
                return None
            except Exception as e:
                print(f"Erro ao avaliar a imagem: {e}")