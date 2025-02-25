from flask import Flask, request, jsonify
import torch
from PIL import Image
import io
import os
import datetime
import numpy as np

app = Flask(__name__)

# Carrega o modelo YOLOv5
model = torch.hub.load('C:/Users/note/Documents/ProjetosRepo/bengala-fecaf/server/yolov5/yolov5-master', 'custom', path='yolov5s.pt', source='local')

# Diretório base para salvar as imagens processadas
BASE_DIR = 'C:/Users/note/Documents/ProjetosRepo/bengala-fecaf/server/yolov5/fotos/'

@app.route('/processar', methods=['POST'])
def processar_imagem():
    if 'image/jpeg' in request.headers.get('Content-Type', ''):
        img_bytes = request.data
        img = Image.open(io.BytesIO(img_bytes))
        results = model(img, size=640)

        # Exibir os resultados no terminal
        print("Resultados da Detecção:")
        print(results.pandas().xyxy[0])  # Exibe os resultados em formato de DataFrame

        # Salvar a imagem com os resultados
        os.makedirs(BASE_DIR, exist_ok=True)  # Cria o diretório 'processed_images' se não existir
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(BASE_DIR, f"processed_image_{timestamp}.jpg")

        # Renderizar e salvar a imagem com bounding boxes
        results.render()  # Renderiza as caixas delimitadoras na imagem
        img_np = np.squeeze(results.render())  # Converte a imagem renderizada em um array numpy
        img_pil = Image.fromarray(img_np)
        img_pil.save(output_path)  # Salva a imagem como um arquivo

        # Retornar os resultados em formato JSON
        detections = results.pandas().xyxy[0].to_json(orient="records")
        return detections
    else:
        return jsonify({'error': 'Tipo de conteúdo não suportado'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
