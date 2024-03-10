from ultralytics import YOLO
import cv2;
import os;
import time;
import serial;

# Change the port name to match the port used by your Arduino
port = '/dev/cu.usbmodem101'
baud_rate = 9600

# Open serial port
arduino = serial.Serial(port, baud_rate, timeout=1)
time.sleep(2)  # Allow time for Arduino to reset after connection

dir_path = 'img'
baseName = 'camera_capture'
base_path = os.path.join(dir_path, baseName)
start = time.time()
classNames = ['BIODEGRADABLE', 'CARDBOARD', 'GLASS', 'METAL', 'PAPER', 'PLASTIC']


def save_frame_camera_key(device_num, dir_path, base_path, ext='jpg', delay=1, window_name='frame'):
    cap = cv2.VideoCapture(device_num)
    count=0
    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)

    while True:

        current_time = time.time()
    
        ret, frame = cap.read()
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(delay) & 0xFF
        # if key == ord('c'):
        #     cv2.imwrite('{}_{}.{}'.format(base_path, 1, ext), frame)
        #     break

        if count > 250: #turn off camera after a certain time
            cv2.imwrite('{}_{}.{}'.format(base_path, 1, ext), frame)
            break

        count+=1

    cv2.destroyWindow(window_name)


def createModel(): #this function creates the model
    model = YOLO("yolo-Weights/best.pt")

    results = model('img/camera_capture_1.jpg')

    classNames_of_elements_Scanned = []

    for r in results:
        boxes = r.boxes

        for box in boxes:
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            classNames_of_elements_Scanned.append(classNames[cls])

    print(f"The model has detected: {classNames_of_elements_Scanned}")

    return classNames_of_elements_Scanned

#sort to classes. Recyling, GARBAGE, OR COMPOST -> GIVE TO ARDUINO 0, 1, 2
#'BIODEGRADABLE', 'CARDBOARD', 'GLASS', 'METAL', 'PAPER', 'PLASTIC'


def filterResult(classNames_from_firstScan): #function for error checking

    #if result has multiple items with different categories
    if len(classNames_from_firstScan) > 1:
        print("Sorry! Only one item at a time. Please separate items")
        save_frame_camera_key(0, dir_path, base_path)
        classNames_from_firstScan = createModel()

        if len(classNames_from_firstScan) > 1: #if user places two items again - itll just take the first element
            print("Scan performed again and received multiple items. Only one is taken")
            classNames_from_firstScan = classNames_from_firstScan[:1]

    return classNames_from_firstScan


def assignArduinoResult(classArray): #this function assigns the numerical value based off the classname
    arduinoResult = ''
    for item in classArray:
        if item == 'BIODEGRADABLE': #compost
            arduinoResult = '2'
        
        elif item == 'CARDBOARD' or item == 'PAPER': #recycling
            arduinoResult = '1'

        elif item == 'GLASS' or item == 'METAL' or item == 'PLASTIC': #garbage
            arduinoResult = '0'

        else: #just put in garbage >.<
            arduinoResult = '0'

    return arduinoResult

if __name__ == "__main__":

    # Run the model until a non-empty result is obtained
    while True:
        save_frame_camera_key(0, dir_path, base_path)  # Capture frame
        firstScan = set(createModel())  # Run the model
        
        if firstScan:  # If result is not empty
            classArray = filterResult(firstScan)
            if classArray:  # If classArray is not empty
                break  # Exit loop
        else:
            print("No item detected. Please try again")

    # Process the result
    finalResult_forArduino = assignArduinoResult(classArray)

    with open('arduino_result.txt', 'w') as f:
        f.write(str(finalResult_forArduino)) #write the variable value to a text file so it can be read from another file

    print(f"final results {classArray}")
    print(finalResult_forArduino)

    arduino.write(str(finalResult_forArduino).encode())

#---------HOW TO READ value from text file in another file ------------
# with open('arduino_result.txt', 'r') as f:
#     arduinoResult = f.read()
#-----------------------------------------------------------------------



