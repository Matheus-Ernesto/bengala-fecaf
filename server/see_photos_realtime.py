import cv2
import os

# Pasta principal onde as imagens estão salvas
image_folder = "runs"

def get_latest_image(folder):
    # Lista todas as subpastas que seguem o padrão "DD-MM-YYYY_HH-MM-SS-FFF"
    subfolders = [os.path.join(folder, sub) for sub in os.listdir(folder) if os.path.isdir(os.path.join(folder, sub))]

    if not subfolders:
        return None

    # Ordenar as subpastas pelo timestamp no nome (mais recente primeiro)
    subfolders.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    for subfolder in subfolders:
        # Caminho para a pasta "output" dentro da subpasta
        output_folder = os.path.join(subfolder, "output")
        
        if not os.path.exists(output_folder):
            continue  # Se a pasta "output" não existir, pula essa pasta

        # Nome esperado do arquivo .jpg dentro da pasta "output"
        folder_name = os.path.basename(subfolder)
        expected_image_path = os.path.join(output_folder, f"{folder_name}.jpg")

        # Se o arquivo existe, retorna ele
        if os.path.exists(expected_image_path):
            return expected_image_path

    return None

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
