import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import os
import io

# Caminhos das imagens
paths = [
    "images/photos/output.jpg",
    "images/runs_yolo/output.jpg",
    "images/runs_midas/output.png"
]

class ImageUpdater:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualização de Imagens")
        self.root.bind("<q>", lambda e: self.quit())

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.labels = []
        for _ in range(3):
            label = tk.Label(self.frame)
            label.pack(side="left", padx=5)
            self.labels.append(label)

        self.update_images()

    def load_image_safely(self, path, grayscale=False):
        try:
            with open(path, "rb") as f:
                data = f.read()
            img = Image.open(io.BytesIO(data))

            if grayscale:
                img = img.convert("L")
                img = ImageOps.colorize(img, black="black", white="white")  # Pode trocar as cores
            else:
                img = img.convert("RGB")

            img = img.resize((400, 300))
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Erro ao carregar {path}: {e}")
            return None

    def update_images(self):
        for i, path in enumerate(paths):
            if os.path.exists(path):
                is_grayscale = (i == 2)
                tk_img = self.load_image_safely(path, grayscale=is_grayscale)
                if tk_img:
                    self.labels[i].config(image=tk_img)
                    self.labels[i].image = tk_img  # Mantém referência

        self.root.after(1, self.update_images)

    def quit(self):
        self.root.destroy()

# Inicializa a janela
root = tk.Tk()
app = ImageUpdater(root)
root.mainloop()
