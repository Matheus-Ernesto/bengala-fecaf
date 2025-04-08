import os
from ultralytics import YOLO
import torch
import sys
import gc

# Configura o nível de log da biblioteca ultralytics para não exibir mensagens
import logging
logging.getLogger("ultralytics").setLevel(logging.CRITICAL)

from contextlib import contextmanager

# Função para ocultar prints
# Esta função redireciona a saída padrão para um arquivo nulo (devnull) para ocultar prints
@contextmanager
def ocultar_prints():
    stdout_original = sys.stdout
    stderr_original = sys.stderr
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    try:
        yield
    finally:
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = stdout_original
        sys.stderr = stderr_original

# Função para verificar se o modelo já foi carregado
# Esta função verifica se o modelo já foi carregado e, se não, carrega o modelo
class Yolo:
    def __init__(self):
        # Define o modelo a ser utilizado
        self.modelo = "yolov5nu.pt"
        # Variável que armazenará o modelo carregado
        self._model = None

    # Método para treinar o modelo
    # Este método treina o modelo YOLO com os parâmetros fornecidos
    def treinar(self, yaml, qualidade, fatoracao):
        # Carrega o modelo base
        self._model = YOLO(os.path.join("bengalaFecaf","weights",self.modelo))

        # Define se o treinamento usará CUDA (GPU) se disponível, se não usará CPU
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Usando dispositivo: {device}")

        # Treinamento do modelo
        train_results = self._model.train(
            data=yaml,                          # Arquivo com caminho dos dados
            epochs=fatoracao,                   # Número de épocas de treinamento
            imgsz=qualidade,                    # Tamanho da imagem
            device=device,                      # Dispositivo usado
            project="bengalaFecaf/training",    # Local para salvar os resultados
            name="train"                        # Nome do experimento
        )

        # Avaliação do modelo após o treinamento
        metrics = self._model.val()

        return None
    
    # Método para carregar o modelo treinado na memória
    # Este método carrega o modelo YOLO com os pesos fornecidos
    def carregar(self):
        with ocultar_prints():
            self._model = YOLO(os.path.join("bengalaFecaf","weights", self.modelo))
        return None
    
    # Método para fazer a detecção de objetos em uma imagem
    def avaliar(self, image): 
        with ocultar_prints(): # Ocultar mensagens durante a avaliação
            try:
                # Executa o modelo na imagem recebida
                results = self._model(image)

                # Salva a imagem de saída em um diretório específico
                os.makedirs("images/runs_yolo", exist_ok=True)

                # Salva a imagem de saída com os resultados
                # Se não houver resultados, não salva a imagem
                if results and len(results) > 0:
                    results[0].save(filename=os.path.join("images", "runs_yolo", "output.jpg"))

                # Limpa os resultados para liberar memória
                del results
                gc.collect() # Força a limpeza da memória
                return None
            # Se ocorrer um erro durante a avaliação, imprime o erro
            # Isso pode ocorrer se a imagem não for válida ou se o modelo falhar
            except Exception as e:
                print(f"Erro ao avaliar a imagem: {e}")