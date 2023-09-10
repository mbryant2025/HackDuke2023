#serial reading to get temperature and humidity values
import serial

#initialize serial port
def init_serial(port_name, baud_rate = 9600):
    print("Initializing serial port")
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
    temp, humidity = 0,0

    #initialize serial port
    ser = init_serial("COM4")
    print ("Serial port initialized")

    #read serial forever
    while True:
        temp, humidity = read_temp_humidity(ser)
        print("Temperature: " + str(temp) + " Humidity: " + str(humidity))
        #write them to a file
        with open("temp_humidity.txt", "w") as f:
            f.write(str(temp) + "," + str(humidity))