
# Importa servidor
from bengalaFecaf.server import Server
# Importa IA Yolo
from bengalaFecaf.yolo import Yolo
# Importa IA Midas
from bengalaFecaf.midas import Midas

server = Server()
server.yolo = None
server.midas = None
server.verbose = False

server.iniciar()