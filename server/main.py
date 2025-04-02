from bengalaFecaf.server import Server
from bengalaFecaf.yolo import Yolo
from bengalaFecaf.midas import Midas

yolo = Yolo()
midas = Midas()

server = Server()
server.yolo = yolo
server.midas = midas

server.iniciar()