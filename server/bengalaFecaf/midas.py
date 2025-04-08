import sys
import os

# Adiciona o diretório atual ao path do sistema
sys.path.append("midasLib")
sys.path.append("bengalaFecaf/midasLib")

# Importa o módulo run do diretório midasLib
# O módulo run contém funções para carregar o modelo e processar imagens
import run
from contextlib import contextmanager

# Função para ocultar prints
# Esta função redireciona a saída padrão para um arquivo nulo (devnull) para ocultar prints
@contextmanager
def ocultar_prints():
    stdout_original = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    try:
        yield
    finally:
        sys.stdout.close()
        sys.stdout = stdout_original

# Função para verificar se o modelo já foi carregado
class Midas:
    def __init__(self):
        self.modelo = "midas_v21_small_256.pt"
        self.tipo_modelo = "midas_v21_small_256"
        self._model = None
        self.transform = None
        self.net_w = None
        self.net_h = None
    
    # Método para verificar se o modelo já foi carregado
    def carregar(self):
        with ocultar_prints():
            self._model, self.transform, self.net_w, self.net_h, = run.preload(
                "bengalaFecaf/weights/"+self.modelo,
                self.tipo_modelo,
                False,
                None,
                False)
        return None
    
    # Método para avaliar a imagem
    # Este método chama a função run_with_model do módulo run para processar a imagem
    def avaliar(self, imagem):
        with ocultar_prints():
            run.run_with_model(self._model, self.transform, self.net_w, self.net_h, imagem, "images/runs_midas", model_type=self.tipo_modelo, optimize=True, side=False, grayscale=True)
        return None