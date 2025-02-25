import cv2
import os

def capture_imge(data_class):
    image_count = 0
    cap = cv2.VideoCapture(0)
    save_dir = 'img_capture/' + data_class
    
    os.makedirs(save_dir,exist_ok=True)
    
    while True:
        ret, frame = cap.read()
        
        cv2.imshow('Webcam', frame)
        key = cv2.waitKey(1)
        
        if key == ord('c'):
            file_name = f'{save_dir}/img_{image_count}.jpg'
            cv2.imwrite(file_name,frame)
            image_count +=1
            
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

capture_imge('normal')
capture_imge('error')