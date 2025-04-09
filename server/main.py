# Importa servidor
from bengalaFecaf.server import Server
# Importa IA Yolo
from bengalaFecaf.yolo import Yolo
# Importa IA Midas
from bengalaFecaf.midas import Midas

# Cria a IA Midas
midas = Midas()

# Padrão do Midas ---------------------------------------------------------------

# Atribui o nome do modelo que está salvo no bengalaFecaf/weights, por padrão ele utiliza o que já
# vem, o midas_v21_small_256.pt
midas.modelo = "midas_v21_small_256.pt"
# Atribui o tipo do modelo que será usado, por padrão é usado o midas_v21_small_256
midas.tipo_modelo = "midas_v21_small_256"
# Carrega o modelo na RAM
midas.carregar()
# Avalia uma imagem dentro de uma pasta, ou várias dentro de uma pasta
midas.avaliar("images/output/")

# Fim do padrão do Midas --------------------------------------------------------

# Cria a IA Midas
yolo = Yolo()

# Padrão do Midas ---------------------------------------------------------------

# Atribui o nome do modelo que está salvo no bengalaFecaf/weights, por padrão ele utiliza o que já
# vem, o yolov5nu.pt
yolo.modelo = "yolov5nu.pt"
# Carrega o modelo na RAM
yolo.carregar()
# Avalia uma imagem
yolo.avaliar("images/output/output.jpg")

# Fim do padrão do Midas --------------------------------------------------------

server = Server()

# Padrão do servidor ---------------------------------------------------------------

# Atribui o yolo ao servidor, se passado None, o servidor não carregará nenhum Yolo.
server.yolo = yolo
# Atribui o midas ao servidor, se passado None, o servidor não carregará nenhum Midas.
server.midas = midas
# Marca se deseja ver todos os logs ou apenas os FPS.
server.verbose = True

# Fim do padrão do servidor --------------------------------------------------------

# Abre o servidor
# Faz o benchmark offine das ias por 15 segundos
server.benchmark(midas, "images/photos/")
server.benchmark(yolo, "images/photos/output.jpg")

# Inicia o servidor, parando a thread principal nesse comando, nada mais deve ser rodado
# após esse comando, ou deve ser iniciado em outra thread.
server.iniciar()

