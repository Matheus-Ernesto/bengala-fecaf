import os
import shutil

# Pastas a serem limpas
folders_to_clean = ["runs", "photos"]

def clear_folder(folder):
    if os.path.exists(folder):
        for item in os.listdir(folder):
            item_path = os.path.join(folder, item)
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # Remove diretório e todo seu conteúdo
                else:
                    os.remove(item_path)  # Remove arquivo
            except Exception as e:
                print(f"Erro ao remover {item_path}: {e}")
    else:
        print(f"Pasta '{folder}' não encontrada.")

# Limpa todas as pastas da lista
for folder in folders_to_clean:
    clear_folder(folder)
    print(f"Pasta '{folder}' limpa com sucesso!")
