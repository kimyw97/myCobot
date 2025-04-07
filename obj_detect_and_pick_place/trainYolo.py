from ultralytics import YOLO

model = YOLO("/Users/kyw/VSCode/myCobot/obj_detect_and_pick_place/runs/detect/train8/weights/best.pt")
model.train(data='./datasets/color_detection/custom_data.yaml', epochs= 10, patience = 20, batch=2)
model.predict(data='./datasets/color_detection/test/images', save= True)