# Importa servidor
from bengalaFecaf.server import Server
# Importa IA Yolo
from bengalaFecaf.yolo import Yolo
# Importa IA Midas
from bengalaFecaf.midas import Midas

midas = Midas()
yolo = Yolo()

# Cria o servidor
server = Server()

# Padrão do servidor ---------------------------------------------------------------

# Atribui o yolo ao servidor, se passado None, o servidor não carregará nenhum Yolo.
server.yolo = None
# Atribui o midas ao servidor, se passado None, o servidor não carregará nenhum Midas.
server.midas = midas
# Marca se deseja ver todos os logs ou apenas os FPS.
server.verbose = True

# Fim do padrão do servidor --------------------------------------------------------

# Abre o servidor
server.iniciar()

