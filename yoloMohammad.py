from ultralytics import YOLO
import cv2;
import os;

dir_path = 'img'
baseName = 'camera_capture'
base_path = os.path.join(dir_path, baseName)

def save_frame_camera_key(device_num, dir_path, base_path, ext='jpg', delay=1, window_name='frame'):
    cap = cv2.VideoCapture(device_num)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)

    while True:
        ret, frame = cap.read()
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(delay) & 0xFF
        if key == ord('c'):
            cv2.imwrite('{}_{}.{}'.format(base_path, 1, ext), frame)
            break

    cv2.destroyWindow(window_name)

save_frame_camera_key(1, dir_path, base_path) # to test my code, replace the first parameter from 1 to 0 on windows, cuz Mac is dumb

model = YOLO("yolo-Weights/yolov8n.pt")

results = model('img/camera_capture_1.jpg')

print(results)

