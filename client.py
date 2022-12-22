import cv2
# import imutil
import socket
import numpy as np
import base64

HOST = "127.0.0.1"
PORT = 8000
BUFFER_SIZE = 65536

server = (HOST, PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)
s.connect(server)
host_name = socket.gethostname()

s.sendto(b'', server)
s.settimeout(0.2)

# mask filter
subtractor = cv2.createBackgroundSubtractorMOG2(
    history=100, varThreshold=50, detectShadows=True)

end = "q"

while True:
    # receive the datagram
    try:
        packet, _ = s.recvfrom(BUFFER_SIZE)
        data = base64.b64decode(packet, ' /')
        npdata = np.frombuffer(data, dtype=np.uint8)
        frame = cv2.imdecode(npdata, 1)
    # if the transmission is done, close the client
    except:
        s.close()
        print('client close')
        cv2.destroyAllWindows()
        break

    # show the frame to our screen
    mask_frame = subtractor.apply(frame)
    cv2.imshow('Client video with filter', mask_frame)

    # if key = q, quit
    if cv2.waitKey(1) & 0xFF == ord(end):
        s.close()
        cv2.destroyAllWindows()
        break
