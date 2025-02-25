PT-BR
# bengala-fecaf
Um projeto de faculdade. Este projeto é um projeto com Arduino + Servidor que identifica objetos pertos de colidir, usando ESP32 e YOLOV5

(fotos do projeto)

---------

## Motivação

#### Por quê?
(Explicação)

#### Para quem?
(Explicação)

#### Como?
(Explicação)

---------

## Funcionamento

#### Hardware
(Explicação)

#### Software
(Explicação)

#### Arduino
(Explicação)

#### Servidor
(Explicação)

#### O yolov5
(Explicação)

---------

## Como instalar o YOLOV5
(Explicação)

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