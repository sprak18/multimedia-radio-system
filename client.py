import cv2
import time
import socket
import struct
import numpy as np

# Set socket options
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65535)

print("\n Client is Successfully Started")
try:
    inp = input("\n\t --> Type 'start' to Initiate Connection: ")
except KeyboardInterrupt as e:
    print("\n\n Terminated \n\n")
    sock.close()
    exit(1)

try:
    sock.sendto(inp.encode(), (multicast_group, 10000))
    data, address = sock.recvfrom(10000)
except socket.error as e:
    print(f"\n Socket Error \n")
    sock.close()
    exit(1)

data = data.decode()
n1, a, b, c, d, n2, e, f, g, h = data.split(',')

print("\nStation 1")
print(f"Name: {n1}")
print(f"Resolution: {a}x{b}")
print(f"Aspect Ratio: {c}")
print(f"Framerate: {d}")

print("\nStation 2")
print(f"Name: {n2}")
print(f"Resolution: {e}x{f}")
print(f"Aspect Ratio: {g}")
print(f"Framerate: {h}")

print("\n\n Press 'p' to Pause the Video")
dat = 0

try:
    input_value = input("\n Select a Station: \n\t 1) Station 1 \n\t 2) Station 2 \n\n Choice : ")
except KeyboardInterrupt as e:
    print("\n Terminated \n")
    exit(1)

if len(input_value) > 1:
    print("\n Invalid Input \n")
    exit(1)

dat = input_value
input_value = input_value.encode()

# Send input to server
sock.sendto(input_value, (multicast_group, 10000))

FPS = 30
sta_dat = 0

while True:
    try:
        # Receive data from multicast group
        data, address = sock.recvfrom(65535)
        # Convert data to frame
        frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
        # Resize frame to original size
        frame = cv2.resize(frame, (int(a), int(b))) if dat == "1" else cv2.resize(frame, (int(e), int(f)))
        # Display frame
        cv2.imshow(n1 if dat == "1" else n2, frame)
        # Calculate time taken to display frame
        display_time = time.time()
        # Delay to stream at original speed
        time.sleep(1/FPS - (time.time() - display_time))

        # Press 'p' to exit
        if cv2.waitKey(1) & 0xFF == ord('p'):
            inp = input("\n\n Available Options \n\n 1) Exit \n 2) Change Station \n 3) Resume \n\n Choice: ")
            if inp == "1":
                print("\n Client Closed")
                break
            elif inp == "2":
                print("\n Change Station")
                change = "2" if dat == '1' else "1"
                dat = str(change)
                print(f"\n Switched to Station - {change}")
                change = change.encode()
                sock.sendto(change, (multicast_group, 10000))
            elif inp == "3":
                print("\n Resumed")
            else:
                print("\n Wrong Input, Hence Exiting...")
                break
    except KeyboardInterrupt:
        print("\n Program Terminated")
        sock.close()
        break

# Release video capture and close window
cv2.destroyAllWindows()
