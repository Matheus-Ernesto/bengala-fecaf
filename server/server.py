from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import uvicorn
import shutil
from pathlib import Path
import datetime

# Este código cria um servidor, acessado no http://localhost:8000/process-image/
# Onde ele recebe as fotos enviadas em requisições no seguinte padrão
# POST form-data file->arquivo.jpg/png...

# As fotos normais são salvas em photos/$nomeDoArquivo.formato
# os processamentos são salvos em runs/$dataCompleta_$horaCompleta/$nomeDoArquivo.formato

# execute o server.py para abrir o servidor e deixar tudo ok
# execute o trainer.py para treinar a IA, para isso deve ser baixado uma lista de imagens COCO, ...
# ... mas normalmente isso é automático. Essas imagens são salvas no local de instalação do seu ...
# ... python, em libs/ultralytics/datasets.

app = FastAPI()

# Carregar o modelo uma vez na memória
model = YOLO("best.pt")

# Definir pasta de upload
UPLOAD_FOLDER = Path("photos")

@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    file_path = UPLOAD_FOLDER / file.filename
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    current_time = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    
    model(str(file_path), save=True, project="runs", name=current_time)
    
    # todo

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)