import sys
import os
import time
import io
import base64
from PIL import Image
import cv2
import asyncio
import websockets

sys.path.append('bengalaFecaf')

class Server:
    def __init__(self):
        self.yolo = None
        self.midas = None
        self.verbose = True
        self._last_request_time = time.time()
    
    def iniciar(self):

        if self.yolo: self.yolo.carregar()
        if self.midas: self.midas.carregar()

        connected_clients = set()

        async def echo(websocket):
            connected_clients.add(websocket)
            print("Novo cliente conectado")
            try:
                async for message in websocket:
                    # current_time = time.time()
                    # elapsed_time_ms = (current_time - self._last_request_time) * 1000
                    # fps = 1000 / elapsed_time_ms if elapsed_time_ms > 0 else 0
                    # self._last_request_time = current_time

                    # print(f"##### Tempo entre requisições: {elapsed_time_ms:.2f} ms | FPS: {fps:.2f} #####")

                    # # Processa a imagem
                    # IMAGE_PATH = "images/photos/output.jpg"
                    # IMAGE_PATH_MIDAS = "images/photos/"
                    # IMAGE_PATH_YOLO = "images/photos/output.jpg"

                    # os.makedirs(os.path.dirname(IMAGE_PATH), exist_ok=True)

                    # image_bytes = base64.b64decode(data)
                    # image = Image.open(io.BytesIO(image_bytes))
                    # image.save(IMAGE_PATH)

                    # if self.verbose:
                    #     print("Imagem salva em:", IMAGE_PATH)

                    # if self.yolo:
                    #     self.yolo.avaliar(IMAGE_PATH_YOLO)

                    # if self.midas:
                    #     self.midas.avaliar(IMAGE_PATH_MIDAS)

                    # image_path = f"images/runs_midas/output-{self.midas.tipo_modelo}.png"
                    # image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

                    # if image is None:
                    #     print("Erro ao carregar a imagem.")
                    #     # await websocket.send("false")
                    # else:
                    #     height, width = image.shape
                    #     crop_x = int(width * 0.2)
                    #     crop_y = int(height * 0.2)
                    #     cropped_image = image[crop_y:height - crop_y, crop_x:width - crop_x]

                    #     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(cropped_image)

                    #     if self.verbose:
                    #         print(f"O pixel mais branco tem valor: {max_val} (escala de 0 a 255)")
                    #         print(f"Localização do pixel mais branco: {max_loc}")

                    #     ativar_motor = max_val >= 200
                    #     await websocket.send("true" if ativar_motor else "false")

                    await websocket.send(f"Echo: {message}")
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Cliente desconectado: {e}")
            finally:
                connected_clients.remove(websocket)

        async def main():
            async with websockets.serve(echo, "192.168.10.4", 8765):
                print("Servidor WebSocket rodando em ws://192.168.10.4:8765")
                await asyncio.Future()

        asyncio.run(main())