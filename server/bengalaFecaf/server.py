import sys
import os

sys.path.append('bengalaFecaf')

from fastapi import FastAPI, Request
import uvicorn
import io
from PIL import Image
import time
import cv2


class Server:
    def __init__(self):
        self.yolo = None
        self.midas = None
        self.last_request_time = time.time()
    
    def iniciar(self):
        app = FastAPI()

        if self.yolo._model is None: self.yolo.carregar()
        if self.midas._model is None: self.midas.carregar()
        
        @app.post("/process-image/")
        async def process_image(request: Request):
            try:
                current_time = time.time()
                elapsed_time_ms = (current_time - self.last_request_time) * 1000
                fps = 1000 / elapsed_time_ms if elapsed_time_ms > 0 else 0
                
                print(f"Tempo entre requisições: {elapsed_time_ms:.2f} ms | FPS: {fps:.2f}")
                
                self.last_request_time = current_time
            
                IMAGE_PATH = "images/photos/output.jpg"
                IMAGE_PATH_MIDAS = "images/photos/"
                IMAGE_PATH_YOLO = "images/photos/output.jpg"

                print("imagem salva em: " + IMAGE_PATH)
                os.makedirs(os.path.dirname(IMAGE_PATH), exist_ok=True)
                img_bytes = await request.body()
                img = Image.open(io.BytesIO(img_bytes))
                img.save(IMAGE_PATH)

                if self.yolo: self.yolo.avaliar(IMAGE_PATH_YOLO)
                if self.midas: self.midas.avaliar(IMAGE_PATH_MIDAS)

                if self.midas:
                    image_path = "images/runs_midas/output-"+self.midas.tipo_modelo+".png"
                    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

                    if image is None:
                        print("Erro ao carregar a imagem.")
                    else:
                        height, width = image.shape
                        crop_x = int(width * 0.2)
                        crop_y = int(height * 0.2)
                        cropped_image = image[crop_y:height-crop_y, crop_x:width-crop_x]
                        
                        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(cropped_image)
                        
                        print(f"O pixel mais branco tem valor: {max_val} (escala de 0 a 255)")
                        print(f"Localização do pixel mais branco: {max_loc}")
                        return {
                            "max_val": max_val,
                        }
                return {
                    "status": "success",
                    "message": "Imagem recebida e erro no processamento"
                }
            
            except Exception as e:
                return {"status": "error", "message": str(e)}
            
        uvicorn.run(app, host="0.0.0.0", port=8000)
        return 0