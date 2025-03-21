from fastapi import FastAPI, Request
from ultralytics import YOLO
import uvicorn
import io
from PIL import Image
import time

app = FastAPI()

model = YOLO("yolov5nu_treinado.pt")

IMAGE_PATH = "photo.jpg"
OUTPUT_PATH = "runs.jpg"

last_request_time = time.time()

@app.post("/process-image/")
async def process_image(request: Request):
    global last_request_time
    try:
        current_time = time.time()
        elapsed_time_ms = (current_time - last_request_time) * 1000
        fps = 1000 / elapsed_time_ms if elapsed_time_ms > 0 else 0
        
        print(f"Tempo entre requisições: {elapsed_time_ms:.2f} ms | FPS: {fps:.2f}")
        
        last_request_time = current_time
        
        img_bytes = await request.body()
        img = Image.open(io.BytesIO(img_bytes))
        img.save(IMAGE_PATH)
        
        results = model(str(IMAGE_PATH))
        if results and len(results) > 0:
            results[0].save(filename=OUTPUT_PATH)
        
        return {
            "status": "success",
            "message": "Imagem processada com sucesso",
            "elapsed_time_ms": round(elapsed_time_ms, 2),
            "fps": round(fps, 2)
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
