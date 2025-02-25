import cv2
import os
import time

# Pasta onde as imagens são salvas
image_folder = "C:/Users/note/Documents/ProjetosRepo/bengala-fecaf/server/yolov5/fotos/"

def get_latest_image(folder):
    """Retorna o caminho da imagem mais recente na pasta."""
    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not files:
        return None
    return max(files, key=os.path.getmtime)  # Pega o arquivo mais recente

def display_latest_image():
    """Mostra sempre a imagem mais recente da pasta."""
    cv2.namedWindow("Stream de Imagens", cv2.WINDOW_NORMAL)

    last_image = None
    while True:
        latest_image = get_latest_image(image_folder)

        if latest_image and latest_image != last_image:
            img = cv2.imread(latest_image)
            if img is not None:
                cv2.imshow("Stream de Imagens", img)
                last_image = latest_image

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Atualiza a cada 500ms e sai com 'q'
            break

    cv2.destroyAllWindows()

display_latest_image()