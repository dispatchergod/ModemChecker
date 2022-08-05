import serial

def send_mk(bits):
    serial_port = serial.Serial(
        port="COM4", baudrate=115200, bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE
    )
    serial_port.write(to_bytes(bits))
    # print(to_bytes(bits))
    (serial_port.readline())
    serial_port.close()

def to_bytes(s):
    return bytes((s).encode("ascii"))

