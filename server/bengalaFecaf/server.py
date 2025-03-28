import threading
import os
import sys

sys.path.append('bengalaFecaf')

from midas import Midas
from yolo import Yolo
from fastapi import FastAPI, Request
from ultralytics import YOLO
import uvicorn
import io
from PIL import Image
import time

class Server:
    def __init__(self):
        self.imprimir_dados = True
        self.fps_maximo = 999
        self.salvar_imagens = True
        self.url = "192.168.0.0/process-image/"
        self.porta = "8000"
        self.yolo = Yolo()
        self.midas = Midas()
        self.last_request_time = time.time()  # Atributo da classe

    def iniciar(self):
        app = FastAPI()

        IMAGE_PATH = "images/photos/output.jpg"
        OUTPUT_PATH = "images/runs_yolo/output.jpg"

        # carregar modelos
        self.yolo.carregar()
        self.midas.carregar()

        @app.post("/process-image/")
        async def process_image(request: Request):
            try:
                current_time = time.time()
                elapsed_time_ms = (current_time - self.last_request_time) * 1000
                fps = 1000 / elapsed_time_ms if elapsed_time_ms > 0 else 0
                
                print(f"Tempo entre requisições: {elapsed_time_ms:.2f} ms | FPS: {fps:.2f}")
                
                self.last_request_time = current_time
                
                img_bytes = await request.body()
                img = Image.open(io.BytesIO(img_bytes))
                img.save(IMAGE_PATH)

                # Aqui chamamos a função para rodar o modelo em outra thread
                thread = threading.Thread(target=self.yolo.avaliar, args=())
                thread.start()

                thread = threading.Thread(target=self.midas.avaliar, args=())
                thread.start()
                
                return {
                    "status": "success",
                    "message": "Imagem recebida e processamento iniciado",
                    "elapsed_time_ms": round(elapsed_time_ms, 2),
                    "fps": round(fps, 2)
                }
            
            except Exception as e:
                return {"status": "error", "message": str(e)}

        # Rodar o servidor FastAPI
        uvicorn.run(app, host="0.0.0.0", port=8000)
        return 0