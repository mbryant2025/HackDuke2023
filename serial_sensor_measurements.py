#serial reading to get temperature and humidity values
import serial

#initialize serial port
def init_serial(port_name, baud_rate = 9600):
    #configure the serial connection
    ser = serial.Serial()
    ser.port = port_name
    ser.baudrate = baud_rate
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
    temp, humidity = line.split(",")
    temp = float (temp)
    humidity = float (humidity)
    return temp, humidity

def read_temp_humidity(ser):
    line = read_serial(ser)
    temp, humidity = parse_temp_humidity(line)
    return temp, humidity

if __name__ == "__main__":
    #initialize serial port
    ser = init_serial("COM4")

    #read serial forever
    while True:
        temp, humidity = read_temp_humidity(ser)
        print("Temperature: " + str(temp) + " Humidity: " + str(humidity))
        if temp > 100:
            print("WARNING: HIGH TEMPERATURE")
        if humidity > 60:
            print("WARNING: HIGH HUMIDITY")