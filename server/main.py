from bengalaFecaf.server import Server
from bengalaFecaf.yolo import Yolo
from bengalaFecaf.midas import Midas

# Este código é um exemplo com todas as funções disponíveis sendo usadas.
# Yolo:
# Neste exemplo, estamos treinando o yolo com a versão YOLOV6N, em uma qualidade media e uma unica fatoração

# não esqueça de baixar o dpt_large_384.pt!
# dpt_large_384.pt: https://github.com/isl-org/MiDaS/releases/download/v3/dpt_large_384.pt
# yolov5nu_treinado - já está na pasta.

yolo = Yolo()
yolo.modelo = "yolov6n.pt"
yolo.tipo_modelo = "yolov6n"
yolo.carregar()
yolo.treinar(yaml="coco8.yaml",qualidade=320, fatoracao=1)

# Midas
# Neste exemplo, o Midas é carregado para a memória e avalia o images/photos/output.jpg
midas = Midas()
midas.carregar()
midas.avaliar()

# Isso inicia o servidor com o yolo e midas padrão, mas se quiser basta trocar o self.yolo do server por sua IA criada
# exemplo: server.yolo = yolo_novo
server = Server()
server.iniciar()