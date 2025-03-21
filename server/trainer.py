from ultralytics import YOLO

model = YOLO("yolov5nu.pt")

train_results = model.train(
    data="coco.yaml",
    epochs=100,
    imgsz=640,
    device="cpu",
)
metrics = model.val()