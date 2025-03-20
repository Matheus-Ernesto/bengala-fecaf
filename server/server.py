from fastapi import FastAPI, Request
from ultralytics import YOLO
import uvicorn
import shutil
from pathlib import Path
import datetime
import io
from PIL import Image
import time  # Adicionado para medir tempo

app = FastAPI()

# Carregar o modelo YOLO
model = YOLO("yolov5nu_treinado.pt")

# Definir pasta de upload
UPLOAD_FOLDER = Path("photos")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# Variável para armazenar o tempo da última requisição
last_request_time = time.time()

@app.post("/process-image/")
async def process_image(request: Request):
    global last_request_time  # Permite modificar a variável global
    try:
        # Medir tempo atual e calcular tempo desde a última requisição
        current_time = time.time()
        elapsed_time_ms = (current_time - last_request_time) * 1000  # Converter para ms
        fps = 1000 / elapsed_time_ms if elapsed_time_ms > 0 else 0  # Calcular FPS
        
        print(f"Tempo entre requisições: {elapsed_time_ms:.2f} ms | FPS: {fps:.2f}")
        
        # Atualizar tempo da última requisição
        last_request_time = current_time
        
        # Ler os bytes da imagem recebida
        img_bytes = await request.body()
        img = Image.open(io.BytesIO(img_bytes))
        
        # Criar nome de arquivo
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S-%f")[:-3]
        file_path = UPLOAD_FOLDER / f"{timestamp}.jpg"
        img.save(file_path)
        
        # Criar diretório para os resultados
        output_dir = Path("runs") / timestamp
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Processar a imagem com YOLO
        model(str(file_path), save=True, project=str(output_dir), name="output")
        
        return {
            "status": "success",
            "message": "Imagem processada com sucesso",
            "output_path": str(output_dir),
            "elapsed_time_ms": round(elapsed_time_ms, 2),
            "fps": round(fps, 2)
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
