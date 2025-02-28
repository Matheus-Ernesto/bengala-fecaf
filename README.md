PT-BR
# bengala-fecaf
Um projeto de faculdade. Este projeto é um projeto com Arduino + Servidor que identifica objetos pertos de colidir, usando ESP32 e YOLOV5

(fotos do projeto)

---------

## Motivação

#### Por quê?
Surge da necessidade de aumentar a autonomia, segurança e acesibilidade para pessoas com deficiência visual. Promove inclusão social, reduzindo riscos e facilitando a locomoção.

#### Para quem?
Deficientes visuais

#### Como?
(Explicação)

---------

## Funcionamento

#### Hardware
(Explicação)

#### Software


#### Arduino
Configura o ESP32-CAM (AI-Thinker) para capturar imagens e enviá-las para o servidor Flask.
    • Conecta-se ao Wi-Fi usando o SSID e password
    • Inicializa a câmera, ajustando brilho, contraste e qualidade da imagem.
    • Captura imagens a cada 17ms e envia para o servidor Flask:
    1. O ESP tira uma foto usando a câmera.
    2. Converte a imagem para o formato JPEG.
    3. Envia a imagem via HTTP POST para http://192.168.10.5/processar
    4. Exibe no Serial Monitor a resposta do servidor 

#### Servidor
Recebe imagens enviadas pelo ESP32-CAM.
Utiliza a biblioteca torch para carregar o modelo YOLOv5
Servidor: http://192.168.10.5/processar
    1. Converte a imagem recebida para um formato que o modelo possa usar.
    2. Processa a imagem com o YOLOv5 para detectar objetos.
    3. Exibe os resultados no terminal.
    4. Salva a imagem processada com as detecções.

#### O yolov5
Realiza a detecção de objetos nas fotos enviadas.
    • O YOLOv5 carrega o modelo de detecção (yolov5s.pt)

Geração e armazenamento das imagens
    • YOLOv5 desnha bounding boxes nos objetos detectados
    • A imagem é salva no diretório fotos/

---------

## Como instalar o YOLOV5
1. Instalar Python 3.10 ou superior
2. Criar um ambiente virtual (opcional)
3. Instalar o YOLOv5
    • git clone https://github.com/ultralytics/yolov5
    • pip install -r requirements.txt

O YOLOv5 oferece diferentes tamanhos de modelos (s, m, l, x)
Para baixar o modelo yolov5s.pt, utilize o comando:
`python -c "from yolov5 import YOLOv5; model = YOLOv5('yolov5s.pt')"`

**(IMPORTANTE)**
Verificar se o PyTorch está utilizando a GPU (se disponível)
Caso tenha uma GPU compatível com CUDA, pode verificar se o PyTorch está detectando a GPU com o seguinte código:
```
import torch
print(torch.cuda.is_available()) # Deve retornar True se houver uma GPU disponível
```

---------

# PONTOS IMPORTANTES A CONFIGURAR ANTES DE EXECUTAR

## Instalar todos os pacotes necessários

## Mudar os paths dos arquivos

Pasta aonde salvará as fotos com cálculo yolo:
Local: app.py -> BASE_DIR = 'C:/Users/note/Documents/ProjetosRepo/bengala-fecaf/fotos/'
Path comum:BASE_DIR = 'C:/Users/<seu usuário>/<pasta do projeto>/fotos/'

Pasta do modelo a ser utilizado (esse por exemplo é o yolov5-master, baixado o zip do github).
Local: app.py -> model = torch.hub.load('C:/Users/note/Documents/ProjetosRepo/bengala-fecaf/yolov5', 'custom', path='yolov5s.pt', source='local')
Path comum:model = torch.hub.load('C:/Users/<seu usuário>/pasta do projeto<>/server/yolov5', 'custom', path='yolov5s.pt', source='local')