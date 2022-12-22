import cv2
import socket
import numpy as np
import base64
import pyautogui

HOST = "127.0.0.1"
# HOST = "192.168.1.115"
PORT = 8000
BUFFER_SIZE = 65536

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )
s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)
host_name = socket.gethostname()
s.bind((HOST, PORT))

#mask filter
subtractor = cv2.createBackgroundSubtractorMOG2(
    history=100, varThreshold=50, detectShadows=True)

cap = cv2.VideoCapture('V&H.mp4')
end = "q"
imageIdx = 0
while True:
    _, client_addr = s.recvfrom(BUFFER_SIZE)
    print('Connection')

    while (cap.isOpened()):
        # read video
        ret, frame = cap.read()

        # send video
        try:
            cv2.imshow('Server original video', frame)
            encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 10])
        except:
            s.close()
            cv2.destroyAllWindows()
            break
        msg = base64.b64encode(buffer)
        s.sendto(msg, client_addr)
        
        #mask filter
        mask_frame = subtractor.apply(frame)
        cv2.imshow('Server video with filter', mask_frame)
            
        #if key = q, quit
        if cv2.waitKey(1) & 0xFF == ord(end):
            s.close()
            cv2.destroyAllWindows()
            break
        #if key = c, screenshot
        if cv2.waitKey(1) & 0xFF == ord('c'):
            image = pyautogui.screenshot()
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv2.imwrite("screenshot"+str(imageIdx)+".png", image)
            imageIdx+=1
            # image.save('screenshot.png')
            print('screenshot')
    break
cap.release()

