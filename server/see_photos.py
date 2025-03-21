import cv2

def display_image(image_path):
    cv2.namedWindow("Stream de Imagens", cv2.WINDOW_NORMAL)
    
    while True:
        img = cv2.imread(image_path)
        if img is not None:
            cv2.imshow("Stream de Imagens", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Sai com SHIFT + 'q'
            break
    
    cv2.destroyAllWindows()

image_path = "photo.jpg"

display_image(image_path)
