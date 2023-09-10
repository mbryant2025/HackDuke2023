#serial reading to get temperature and humidity values
import serial

#initialize serial port
def init_serial(port_name, baud_rate = 9600):
    #configure the serial connection
    ser = serial.Serial()
    ser.port = port_name
    ser.baudrate = baud_rate
    #print(ser)
    ser.open()
    return ser

#read serial output lines 
def read_serial(ser):
    #read serial
    line = ser.readline()
    #convert to string
    line = line.decode("utf-8")
    #print(line)
    return line

def parse_temp_humidity(line):
    #parse temperature and humidity values
    temp = line.split(",")[0]
    humidity = line.split(",")[1]
    return temp, humidity

#initialize serial port
ser = init_serial("COM4")

#read serial
while True:
    line = read_serial(ser)
    temp, humidity = parse_temp_humidity(line)
    print("Temperature: " + temp + ", Humidity: " + humidity)