from ultralytics import YOLO

model = YOLO('yolov8n.pt')
model.train(data='./datasets/error_detection/custom_data.yaml', epochs= 100, patience = 20, batch=5)
model.predict(data='./datasets/error_detection/test/images', save= True)