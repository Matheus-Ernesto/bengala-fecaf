# Importações necessárias
import sys                # Manipulação de caminhos e argumentos do sistema
import time               # Controle de tempo e cálculo de FPS
import asyncio            # Trabalhar com operações assíncronas
import websockets         # Comunicação via WebSocket
import os                 # Manipulação de diretórios e arquivos
import cv2                # OpenCV: processamento de imagem

# Adiciona a pasta 'bengalaFecaf' ao caminho de importação
sys.path.append('bengalaFecaf')

# Classe principal do servidor WebSocket
class Server:
    def __init__(self):
        # Modelos de IA (YOLO e MiDaS)
        self.yolo = None
        self.midas = None

        # Verbosidade ativa: exibe mais informações no terminal
        self.verbose = True

        # Tempo da última requisição (para cálculo de FPS)
        self._last_request_time = time.time()
    
    # Função que inicia o servidor
    def iniciar(self):

        # Carrega os modelos, se definidos
        if self.yolo: self.yolo.carregar()
        if self.midas: self.midas.carregar()

        # Conjunto para manter rastreamento de clientes conectados
        connected_clients = set()

        # Função chamada sempre que um novo cliente se conecta
        async def echo(websocket):
            connected_clients.add(websocket)
            print("Novo cliente conectado")

            try:
                # Loop para escutar mensagens (imagens) do cliente
                async for message in websocket:
                    print("Imagem recebida! Salvando...")

                    # Cria o diretório de imagens, se ainda não existir
                    output_dir = "images/photos"
                    os.makedirs(output_dir, exist_ok=True)

                    # Salva a imagem recebida
                    with open(os.path.join(output_dir, "output.jpg"), "wb") as f:
                        f.write(message)

                    # Calcula o tempo entre requisições e o FPS
                    current_time = time.time()
                    elapsed_time_ms = (current_time - self._last_request_time) * 1000
                    fps = 1000 / elapsed_time_ms if elapsed_time_ms > 0 else 0
                    self._last_request_time = current_time

                    print(f"##### Tempo entre requisições: {elapsed_time_ms:.2f} ms | FPS: {fps:.2f} #####")

                    # Caminhos para processamento das imagens
                    IMAGE_PATH = "images/photos/output.jpg"
                    IMAGE_PATH_MIDAS = "images/photos/"
                    IMAGE_PATH_YOLO = "images/photos/output.jpg"

                    if self.verbose:
                        print("Imagem salva em:", IMAGE_PATH)

                    # Avalia com YOLO (detecção de objetos)
                    if self.yolo:
                        self.yolo.avaliar(IMAGE_PATH_YOLO)

                    # Avalia com MiDaS (profundidade)
                    if self.midas:
                        self.midas.avaliar(IMAGE_PATH_MIDAS)

                    # Caminho da imagem de profundidade gerada pelo MiDaS
                    image_path = f"images/runs_midas/output-{self.midas.tipo_modelo}.png"
                    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Lê em tons de cinza

                    if image is None:
                        print("Erro ao carregar a imagem.")
                        # Aqui poderia-se enviar uma mensagem de erro ao cliente
                        # await websocket.send("false")
                    else:
                        # Corta as bordas da imagem para remover ruído
                        height, width = image.shape
                        crop_x = int(width * 0.2)
                        crop_y = int(height * 0.2)
                        cropped_image = image[crop_y:height - crop_y, crop_x:width - crop_x]

                        # Encontra o pixel mais claro (mais próximo)
                        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(cropped_image)

                        if self.verbose:
                            print(f"O pixel mais branco tem valor: {max_val} (escala de 0 a 255)")

                        # Se o pixel mais claro for acima de um limiar, ativa o motor
                        ativar_motor = max_val >= 200
                        await websocket.send("true" if ativar_motor else "false")

                    # Mensagem de confirmação para o cliente
                    await websocket.send("Imagem recebida e salva com sucesso!")

            except websockets.exceptions.ConnectionClosed as e:
                print(f"Cliente desconectado: {e}")
            finally:
                # Remove cliente da lista de conectados ao desconectar
                connected_clients.remove(websocket)

        # Função principal do servidor
        async def main():
            # Inicia o servidor WebSocket no IP local e porta 8765
            async with websockets.serve(echo, "192.168.10.4", 8765):
                print("Servidor WebSocket rodando em ws://192.168.10.4:8765")
                await asyncio.Future()  # Mantém o servidor rodando para sempre

        # Roda o servidor WebSocket
        asyncio.run(main())

    def benchmark(self, ia, path):
        contador = 0
        inicio = time.time()
        ia.carregar()
        contador_escape = 0
        print(f"Avaliando {ia.modelo}")

        while True:
            ia.avaliar(path)
            contador += 1
            agora = time.time()

            if agora - inicio >= 1:  # passou 1 segundo
                print(f"{contador} avaliações por segundo")
                contador_escape += 1
                contador = 0
                inicio = agora

            if contador_escape >= 15:
                print(f"Saindo do benchmark, {ia.modelo} avaliado")
                return
