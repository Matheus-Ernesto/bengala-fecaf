PT-BR
# bengala-fecaf
Projeto com Arduino + Servidor que identifica objetos pertos de colidir, usando ESP32 e YOLOv11.

(fotos do projeto)

---------

## Motivação

Pessoas com deficiência visual enfrentam desafios diários para se locomover com segurança. Apesar das bengalas e cães-guia, obstáculos inesperados ainda representam riscos. Esse projeto visa oferecer uma solução acessível e eficiente para detecção de objetos próximos, alertando os usuários antes de uma possível colisão.

#### Por quê?
Surge da necessidade de aumentar a autonomia, segurança e acessibilidade para pessoas com deficiência visual, além de promover a inclusão social, reduzindo riscos e facilitando a locomoção.

#### Para quem?
Deficientes visuais, Este sistema é projetado para pessoas cegas ou com baixa visão, auxiliando na mobilidade segura em ambientes internos e externos.

#### Como?
O projeto consiste em um equipamento com dois sensores, sendo o sensor ultrassônico HCSR04, que permite detectar distâncias até 4 metros, e uma câmera ESP32, que captura as imagens, e usando a internet, envia elas ao servidor, este servidor processa as imagens com o YOLO11 e retorna ao ESP32 avisando se tem objetos próximos na imagem ou não. Além dos sensores, o equipamento conta com um motor de vibração para alertar o usuário se tiver objetos perto, vibrando a bengala, e sua bateria (uma pilha de 9V). Para melhor teste do equipamento, ele também utiliza dois LEDs, um para trâfego e indicação de resultados no código, outro para erros e saber se está ligado corretamente.

---------

## Funcionamento

1. O ESP32 faz a leitura do sensor ultrassônico HCSR04, verificando se ele indentificou objetos próximos.

2. ESP32-CAM captura imagens a cada 17ms e as envia para um servidor FastAPI/Flask via Wi-Fi (neste projeto, a rede é LAN).

3. Servidor processa as imagens usando YOLOv11, detectando objetos.

4. Se tiver objetos perto, é indicado pela vibração no dispositivo.


#### Hardware

Componentes do Hardware:
- ESP32: Câmera e mini arduino, sendo programável em C# pelo Arduino IDE (Precisa de conversor UART).
- Sensor ultrassônico HCSR04: Sensor ultrassônico com trigger e echo, um dos mais famosos e utilizados.
- Motor cc: Um mini motor cc, simples, ligado ao ESP32 por meio de um transistor NPN (BCE) para não ter problemas de corrente elétrica.
- LEDs: Luzes apenas para testes e verificação de erros.
- Bateria: Bateria 9V para energizar tudo.

#### Software

Softwares que estamos usando e bibliotecas/repositórios:

- YOLO 11: IA de reconhecimento de objetos na imagem.
- ml-depth: IA de profundidade baseada em imagens únicas.
- Flask/FastAPI: Forma de comunicação do servidor com requisições do ESP32, este deixa a utilização dos serviços online mais rápido.

#### Arduino

Configura o ESP32-CAM (AI-Thinker) para capturar imagens e enviá-las para o servidor Flask.

* Conecta-se ao Wi-Fi usando o SSID e senha.
* Inicializa a câmera, ajustando brilho, contraste e qualidade da imagem.
* Faz leitura do HCSR04 para saber se tem objetos perto.
* Captura imagens a cada 17ms e envia para o servidor Flask:
1. O ESP tira uma foto usando a câmera.
2. Converte a imagem para o formato JPEG.
3. Envia a imagem via HTTP POST para `http://localhost/processar`.
4. Exibe no Serial Monitor a resposta do servidor.

#### Servidor
Recebe imagens enviadas pelo ESP32-CAM.
* Utiliza a biblioteca `torch` para carregar o modelo YOLOv5.
* Servidor: `http://localhost/processar`.
1. Converte a imagem recebida para um formato que o modelo possa usar.
2. Processa a imagem com o YOLOv5 para detectar objetos.
3. Exibe os resultados no terminal.
4. Salva a imagem processada com as detecções no diretório `fotos/`.

#### YOLOv11
Realiza a detecção de objetos nas fotos enviadas.

* O YOLOv11 carrega o modelo de detecção (`yolo11x.pt`).
* Desenha bounding boxes nos objetos detectados.
* A imagem é salva no diretório `photos/`, e o resultado dos cálculos no `runs/`.

## Melhorias a serem implementadas no semestre 1/2025

1. Melhoria na IA (YOLO): Estamos atualizando do yolo5 para o yolo11, usando uma versão mais potente no servidor e mais precisa.
2. Melhoria no delay: Estamos melhorando o delay do sistema inteiro, para que consiga processar mais imagens e manter uma boa integradade nos sensores.
3. Design: Estamos melhorando o design para que os sensores consigam fazer leituras mais corretas e precisas.
4. Conexões físicas: estamos melhorando as conexões do projeto para que tenha menos problemas físicos com conexões e cabeamentos.

## Próximas melhorias
Estas melhorias podem ser aplicadas neste semestre (1/2025), porém elas são adicionais.

1. Uso do ML-DEPTH-PRO: Utilizar a IA ml-depth, desenvolvida pela Apple, para fazer diretamente o cálculo de objetos próximos com apenas imagens.
2. Uso do Pico 2: Usar o Rasperry PI para processamento direto, sem necessidade do servidor.
3. Design: Diminuir o design e encontrar uma forma que fique os sensores precisos e o desenho agradável, melhorando também o peso e ergonomia.
4. Melhoria no sonar: Trocar o HCSR04 por algum sensor mais potente e preciso, como sensores TOF e Lidar mais robustos.
5. Implementação de um novo sensor: Usar um sensor novo de infravermelho, com precisão atém 1,5 metros, na parte d ebaixo da bengala.

---

# A mexer na parte abaixo.

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