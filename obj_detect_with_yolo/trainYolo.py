from ultralytics import YOLO

model = YOLO('yolov8n.pt')
model.train(data='./datasets/cobot_control/custom_data.yaml', epochs= 30, patience = 20, batch=2)
model.predict(data='./datasets/cobot_control/test/images', save= True)