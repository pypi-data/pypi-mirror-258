import serial
from .screen import _Screen

screen = _Screen()

def bind(usb_port: str):
    """
    Binds the serial port that the VEX Brain is connected to. Necessary before running any VEX commands. \n
    \n Additionally, the port must be opened. This can only be achieved while a program is actively running on the VEX brain. It is recommended that the running program already has any motors, sensors, and controllers predefined.
    :param usb_port: Name of the port, expressed generally as COM followed by the port number. Example: COM3
    """

    try:
        port = serial.Serial(port=usb_port, baudrate=115200)
        screen.port = port

    except serial.serialutil.SerialException:
        raise SystemError("COM Port does not exist. Check if the port is open.")


