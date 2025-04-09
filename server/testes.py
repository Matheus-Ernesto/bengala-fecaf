# Apenas um arquivo de testes, nada demais
from bengalaFecaf.server import Server
from bengalaFecaf.yolo import Yolo
from bengalaFecaf.midas import Midas

server = Server()
server.verbose = False
server.iniciar()