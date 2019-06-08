import serial

ser = serial.Serial('COM3',9600)

while 1:
    while (ser.inWaiting() > 0):
        data = ser.readline().decode().strip()
        print(data)
