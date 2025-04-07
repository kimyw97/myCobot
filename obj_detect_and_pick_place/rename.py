import torch

# 모델 불러오기
checkpoint = torch.load("/Users/kyw/VSCode/myCobot/obj_detect_and_pick_place/runs/detect/train8/weights/best.pt")

# 클래스 이름 수정
checkpoint['model'].names = ['blue', 'green', 'red', 'yellow']

# 저장
torch.save(checkpoint, "best_fixed.pt")
