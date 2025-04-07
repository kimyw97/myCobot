import os
import cv2
import albumentations as A
import numpy as np

# 경로 설정
image_dir = "./datasets/color_detection/train/images"
label_dir = "./datasets/color_detection/train/labels"
output_image_dir = "./datasets/color_detection/aug/images"
output_label_dir = "./datasets/color_detection/aug/labels"

os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_label_dir, exist_ok=True)

# 증강 파이프라인 정의
transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.3),
    A.ColorJitter(p=0.3),
    A.Rotate(limit=15, p=0.5),
    A.Resize(640, 640),
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

# 증강 수행
for fname in os.listdir(image_dir):
    if not fname.endswith(".jpg"):
        continue

    image_path = os.path.join(image_dir, fname)
    label_path = os.path.join(label_dir, fname.replace(".jpg", ".txt"))

    # 이미지 읽기
    image = cv2.imread(image_path)

    # 라벨 읽기
    if not os.path.exists(label_path):
        continue
    with open(label_path, "r") as f:
        lines = f.read().strip().split("\n")
        boxes = []
        class_labels = []
        for line in lines:
            parts = line.strip().split()
            cls, x, y, w, h = parts
            boxes.append([float(x), float(y), float(w), float(h)])
            class_labels.append(int(cls))

    # 증강 적용
    for i in range(3):  # 한 장당 3개씩 증강
        augmented = transform(image=image, bboxes=boxes, class_labels=class_labels)
        aug_image = augmented["image"]
        aug_boxes = augmented["bboxes"]
        aug_classes = augmented["class_labels"]

        # 저장
        new_fname = fname.replace(".jpg", f"_aug{i}.jpg")
        cv2.imwrite(os.path.join(output_image_dir, new_fname), aug_image)

        # 라벨 저장
        with open(os.path.join(output_label_dir, new_fname.replace(".jpg", ".txt")), "w") as f:
            for cls, bbox in zip(aug_classes, aug_boxes):
                x, y, w, h = bbox
                f.write(f"{cls} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")
