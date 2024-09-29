import cv2
import time
import struct
import socket
import numpy as np
from select import select
from videoprops import get_video_properties

multicast_group = '224.1.1.1'
server_address = ('', 10000)

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
except socket.error as e:
    print(f"\n Socket Error Occurred: {e} \n")
    exit(1)

if(data1 != "start"):
    print("\n Can't Connect, Bye !!! \n")
    exit(1)
else:
    input_value = ("example.mp4" + "," + str(width_1) + "," + str(height_1) + "," +
                   str(Ratio_1) + "," + str(Frame_1) + "," + "Big_Bunny.mp4" + "," +
                   str(width_2) + "," + str(height_2) + "," + str(Ratio_2) + "," + str(Frame_2))
    input_value = input_value.encode()

try:
    sock.sendto(input_value, (multicast_group, 10001))
except socket.error as e:
    print("\n Socket Error \n")
    exit(1)

data, address = sock.recvfrom(65535)  # Use Maximum Buffer Size of 65535
data = data.decode()

if(len(choice) > 1):
    print("\n Kindly, Restart Server for New Client \n")
    exit(1)

print(f"\n initial : User Selected Station - {choice}")

if(choice == '1'):
    cap = cv2.VideoCapture('example.mp4')
elif(choice == '2'):
    cap = cv2.VideoCapture('Big_Bunny.mp4')
else:
    print("\n No Station Selected \n")
    exit(1)

FPS = 30
inpv = 5
timeout = 0.0001  # Timeout in Seconds

while True:
    try:
        ready, _, _ = select([sock], [], [], timeout)
    except:
        print("\n Program Terminated \n")
        exit(1)

    if ready:
        try:
            inpv = ''
            inpv, address = sock.recvfrom(65535)
            data = str(inpv)
            if not inpv:
                break
            if(len(inpv) > 1):
                print("\n\n Terminating ... \n")
                print("\n --> Try to Restart the Server \n")
                exit(1)
            inpv = inpv.decode()
            print(f"\n updated : User Selected Station - {inpv}")
            if inpv == '1':
                cap = cv2.VideoCapture('example.mp4')
            elif inpv == '2':
                cap = cv2.VideoCapture('Big_Bunny.mp4')
        except socket.error as e:
            print(f"\n Socket Error Occurred: {e} \n")
            exit(1)

    try:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # Check if video has ended
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        # Resize frame to fit within maximum packet size
        frame = cv2.resize(frame, (320, 240))
        # Convert frame to string
        data = cv2.imencode('.jpg', frame)[1].tobytes()
        # Send data to multicast group
        sock.sendto(data, (multicast_group, 10001))
        # Calculate time taken to send frame
        send_time = time.time()
        # Delay to stream at original speed
        time.sleep(1/FPS - (time.time() - send_time))
    except KeyboardInterrupt:
        # Clean up the socket
        sock.close()
        break
