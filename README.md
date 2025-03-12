PT-BR
# bengala-fecaf
Projeto com Arduino + Servidor que identifica objetos pertos de colidir, usando ESP32 e YOLOV5

(fotos do projeto)

---------

## Motivação

Pessoas com deficiência visual enfrentam desafios diários para se locomover com segurança. Apesar das bengalas e cães-guia, obstáculos inesperados ainda representam riscos. Seu projeto visa oferecer uma solução acessível e eficiente para detecção de objetos próximos, alertando os usuários antes de uma possível colisão.

#### Por quê?
Surge da necessidade de aumentar a autonomia, segurança e acesibilidade para pessoas com deficiência visual. Promove inclusão social, reduzindo riscos e facilitando a locomoção.

#### Para quem?
Deficientes visuais, Este sistema é projetado para pessoas cegas ou com baixa visão, auxiliando na mobilidade segura em ambientes internos e externos.

#### Como?
(Explicação)

---------

## Funcionamento

1. ESP32-CAM captura imagens a cada 17ms e as envia para um servidor Flask via Wi-Fi.

2. Servidor processa as imagens usando YOLOv5, detectando objetos e sua proximidade.

3. Retorno da informação pode ser feito de várias formas:

 - Um aviso sonoro (bip com diferentes intensidades conforme a proximidade do obstáculo).
 - Vibração no dispositivo para indicar a distância e a posição do objeto.
 - Integração com um aplicativo que emite alertas por áudio.


#### Hardware
(Explicação)

#### Software


#### Arduino
Configura o ESP32-CAM (AI-Thinker) para capturar imagens e enviá-las para o servidor Flask.

* Conecta-se ao Wi-Fi usando o SSID e password.
* Inicializa a câmera, ajustando brilho, contraste e qualidade da imagem.
* Captura imagens a cada 17ms e envia para o servidor Flask:
1. O ESP tira uma foto usando a câmera.
2. Converte a imagem para o formato JPEG.
3. Envia a imagem via HTTP POST para `http://192.168.10.5/processar`.
4. Exibe no Serial Monitor a resposta do servidor.

#### Servidor
Recebe imagens enviadas pelo ESP32-CAM.
* Utiliza a biblioteca `torch` para carregar o modelo YOLOv5.
* Servidor: `http://192.168.10.5/processar`.
1. Converte a imagem recebida para um formato que o modelo possa usar.
2. Processa a imagem com o YOLOv5 para detectar objetos.
3. Exibe os resultados no terminal.
4. Salva a imagem processada com as detecções no diretório `fotos/`.

#### YOLOv5
Realiza a detecção de objetos nas fotos enviadas.

* O YOLOv5 carrega o modelo de detecção (`yolov5s.pt`).
* Desenha bounding boxes nos objetos detectados.
* A imagem é salva no diretório `fotos/`.

---

## Como instalar o YOLOv5
1. Instalar Python 3.10 ou superior.
2. Criar um ambiente virtual (opcional).
3. Instalar o YOLOv5:
    * `git clone https://github.com/ultralytics/yolov5`
    * `pip install -r requirements.txt`

O YOLOv5 oferece diferentes tamanhos de modelos (s, m, l, x).

Para baixar o modelo `yolov5s.pt`, utilize o comando:

<pre><code>python -c "from yolov5 import YOLOv5; model = YOLOv5('yolov5s.pt')"</code></pre>

**IMPORTANTE**
Verifique se a GPU está disponível e pode ser usada com CUDA.
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

Como simplemente colocar para funcionar?

Se quiser rodar rapidamente, basta abrir o cmd nesta pasta e executar o comando:
py ./server.py
Algumas instalações do python tem variações, então pode ser py, py3 e as vezes python.

Isso já inicializará o servidor, ai é só fazer o esp32 conectar a rede wifi e mandar as imagens ao seu ip.
Não sabe seu IP? Tudo bem, basta abrir o cmd, e usar tal comando:
ipconfig
O IP que você deve substituir no código do arduino é o ipv4, tem mais instrucoes no codigo do arduino.