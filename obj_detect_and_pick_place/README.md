<!-- @format -->

## 🦾 myCobot을 활용한 객체 인식 및 집어서 옮기기 프로젝트

이 프로젝트는 **myCobot 로봇 팔**을 사용하여 **YOLOv8 기반 객체 인식**을 수행하고, 인식된 **컬러 블록을 자동으로 집어서 옮기는 기능**을 구현한 예제입니다.

### 📁 디렉토리 구조

```
obj_detect_and_pick_place/
├── block_mover.py                # 블록을 집고 옮기는 메인 로직
├── cobot_control_for_cap_img.py # 이미지 캡처 및 로봇 제어
├── test_with_cam.py             # 웹캠을 활용한 객체 인식 테스트
├── trainYolo.py                 # YOLOv8 학습 스크립트
├── yolov8n.pt                   # 학습된 YOLOv8 모델 가중치
├── augmentation.py              # 데이터 증강 스크립트
├── rename.py                    # 모델 클래스 명 수정
├── README.md                    # 프로젝트 설명 파일
```

### 🧠 주요 기능

- **YOLOv8 기반 실시간 객체 인식**
- **myCobot 로봇 팔을 이용한 블록 집기 및 옮기기**
- 사용자 맞춤 **컬러 블록 인식 모델 학습 파이프라인**
- **웹캠 연동 테스트 기능**
- 데이터 증강 및 리네이밍 유틸리티 제공

### 🚀 실행 방법

1. **환경 설정**

   - Python >= 3.8 필요
   - 의존성 설치:
     ```bash
     pip install -r requirements.txt
     ```

2. **YOLO 모델 학습 (선택사항)**

   ```bash
   python trainYolo.py
   ```

3. **웹캠으로 객체 인식 테스트**

   ```bash
   python test_with_cam.py
   ```

4. **집고 옮기기 실행**
   ```bash
   python block_mover.py
   ```

### 🛠 필요 패키지

- Python
- OpenCV
- [ultralytics](https://github.com/ultralytics/ultralytics) (YOLOv8)
- myCobot SDK

### 🎯 프로젝트 목표

이 프로젝트의 궁극적인 목표는 다음과 같은 로봇 비전 시스템을 구현하는 것입니다:

1. 컬러 블록 인식
2. 위치 판단
3. 로봇팔로 집기
4. 정해진 위치로 옮기기

### 📸 시연 영상


https://github.com/user-attachments/assets/69581248-c365-4178-961d-ecd1e9533913


### 📂 데이터셋 구축

로봇 + 웹캠을 사용하여 직접 데이터를 수집한 후, `augmentation.py`를 활용해 데이터 증강을 진행합니다.
