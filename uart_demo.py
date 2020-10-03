# Easiest way to install library
#   sudo pip install Jetson.GPIO
#   sudo pip install serial

# Setting user permissions
# Must set in order to use the Jetson library
# Create a new gpio user group. 
# Then add your user to the newly created group.

#   sudo groupadd -f -r gpio
#   sudo usermod -a -G gpio jonny

#!/usr/bin/python3
import Jetson.GPIO as GPIO
import threading
import time
import logging
import serial

print("UART Demonstration Program")

GPIO.setmode(GPIO.BOARD) # 40 pin BOARD layout
#GPIO.setmode(GPIO.BCM)  # Broadcom SoC GPIO numbers
#GPIO.setmode(GPIO.CVM)  # String corresponds to signal names on CVM/CVB connector
#GPIO.setmode(GPIO.TEGRA_SOC)    # String corresponds to signal names on Tegra_SoC

# Confirm mode
mode = GPIO.getmode()
print(mode)

# Pin assignments
uart_tx = 8     # UART2_TXD pin (transmit)
uart_rx = 10    # UART2_RXD pin (receive)
htbt = 12       # LED pin for heartbeat signal

# Variables
interval = 0.001    # 1 Hz = 0.001 sec

# Set channel outputs
GPIO.setup(uart_tx, GPIO.OUT)

# Set channel inputs
GPIO.setup(uart_rx, GPIO.IN)

# Initialize Serial port
serial_port = serial.Serial(
    port="dev/ttyTHS1",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY
)

# Create thread for heartbeat (repeats continuously)
# Implemented as daemon: a process that runs in the background
# A program will wait for a thread to complete before it terminates
# A daemon will shut down when the program exits 
# Set the daemon flag during creation in main
def thread_heartbeat(heartbeat):
    logging.info("Daemon %s: starting", heartbeat)
    while(1):
        logging.info("Daemon %s: Beat High", heartbeat)
        GPIO.output(htbt, GPIO.HIGH)
        #time.sleep(interval)
        logging.info("Daemon %s: Beat Low", heartbeat)
        GPIO.output(htbt, GPIO.LOW)
        #time.sleep(interval)


# Send MAVLink message 
def thread_transmit(transmit):
    msg = "GCS to Drone"
    i = 0
    logging.info("Thread %s: starting", transmit)
    """ MAVLink transmission here """
    # transmit msg 
    while(i < 256):
        logging.info("Thread %s: %s", transmit, i)
        i = i + 1

    logging.info("Thread %s: finishing", transmit)

# The main() will create & start the threads
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H: %M: %S")
    
    logging.info("Main : Establish heartbeat connection")
    h = threading.Thread(target=thread_heartbeat, args=(1,), daemon=True) # Create thread
    h.start()   # Start daemon thread
    logging.info("Main : Heartbeat established")

    logging.info("Main : Establish transmission channel")
    t = threading.Thread(target=thread_transmit, args=(1,)) # Create thread
    t.start()   # Start thread
    t.join()




