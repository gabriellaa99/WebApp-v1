import cv2
import base64
import requests

# Constant
API_PATH = "https://anthracoid-dalmatian-0381.dataplicity.io/api/upload"
USERNAME = "gabriela"
PASSWORD = "25100099"
HARDWARE_DEVICE = "TEST HARDWARE 007"
PLACE = "Test Location"

# Capture Image
cam = cv2.VideoCapture(0)   # 0 -> index of camera
s, img = cam.read()
if s:    # frame captured without any errors
    print("Image Captured")
    cv2.imwrite("dummy.jpg",img) #save image

    img = cv2.imread('dummy.jpg', cv2.IMREAD_COLOR )
    retval, buffer_img= cv2.imencode('.jpg', img)
    
    print("Image Encoded")
    image_base64 = base64.b64encode(buffer_img)

    json_payload = { 
        "username": USERNAME,
        "password": PASSWORD,
        "device_hardware" : HARDWARE_DEVICE,
        "place" : PLACE,
        "image": str(image_base64).replace("b'", "").replace("'", "")
        # "image": str(image_base64)[-50:]
    }

    print(json_payload)
    r = requests.post(API_PATH, json=json_payload)
    print(r.text)

