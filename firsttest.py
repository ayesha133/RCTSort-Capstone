from ultralytics import YOLO

# Load a pretrained YOLO model (recommended for training)
model = YOLO('yolov8l.pt')


# Perform object detection on an image using the model
results = model.predict(source = "0", show = True)
print (results)
