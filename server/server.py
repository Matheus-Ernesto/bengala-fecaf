from fastapi import FastAPI, Request
from ultralytics import YOLO
import uvicorn
import shutil
from pathlib import Path
import datetime
import io
from PIL import Image

app = FastAPI()

# Carregar o modelo YOLO
model = YOLO("yolov5nu_treinado.pt")

# Definir pasta de upload
UPLOAD_FOLDER = Path("photos")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

@app.post("/process-image/")
async def process_image(request: Request):
    try:
        # Ler os bytes da imagem recebida
        img_bytes = await request.body()
        img = Image.open(io.BytesIO(img_bytes))
        
        # Criar nome de arquivo
        current_time = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S-%f")[:-3]
        file_path = UPLOAD_FOLDER / f"{current_time}.jpg"
        img.save(file_path)
        
        # Criar diretório para os resultados
        output_dir = Path("runs") / current_time
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Processar a imagem com YOLO
        model(str(file_path), save=True, project=str(output_dir), name="output")
        
        return {"status": "success", "message": "Imagem processada com sucesso", "output_path": str(output_dir)}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)