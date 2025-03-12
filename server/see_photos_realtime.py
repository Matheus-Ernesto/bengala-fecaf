import cv2
import os

# Pasta principal onde as imagens estão salvas
image_folder = "runs"

def get_latest_image(folder):
    # Obtenha todas as subpastas (data_hora) dentro de 'runs'
    subfolders = [os.path.join(folder, subfolder) for subfolder in os.listdir(folder) if os.path.isdir(os.path.join(folder, subfolder))]

    if not subfolders:
        return None

    # Encontrar o arquivo mais recente dentro de cada subpasta
    latest_image = None
    latest_time = 0

    for subfolder in subfolders:
        # Pega todos os arquivos de imagem dentro da subpasta
        files = [os.path.join(subfolder, f) for f in os.listdir(subfolder) if f.endswith(('.png', '.jpg', '.jpeg'))]
        for file in files:
            file_time = os.path.getmtime(file)  # Tempo de modificação do arquivo
            if file_time > latest_time:  # Se a imagem for mais recente que a anterior
                latest_time = file_time
                latest_image = file

    return latest_image

def display_latest_image():
    cv2.namedWindow("Stream de Imagens", cv2.WINDOW_NORMAL)

    last_image = None
    while True:
        latest_image = get_latest_image(image_folder)

        if latest_image and latest_image != last_image:
            img = cv2.imread(latest_image)
            if img is not None:
                cv2.imshow("Stream de Imagens", img)
                last_image = latest_image

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Sai com 'q'
            break

    cv2.destroyAllWindows()

display_latest_image()
