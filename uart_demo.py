# Easiest way to install the gpio library
#   sudo pip install Jetson.GPIO

# Setting user permissions
# Must set in order to use the Jetson library
# Create a new gpio user group. 
# Then add your user to the newly created group.

#   sudo groupadd -f -r gpio
#   sudo usermod -a -G gpio jonny

import Jetson.GPIO as GPIO
import threading
import time
import logging

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
interval = 1    # 1 second heartbeat 

# Set channel outputs
GPIO.setup(uart_tx, GPIO.OUT)

# Set channel inputs
GPIO.setup(uart_rx, GPIO.IN)

# Create thread for heartbeat (repeats continuously)
def thread_heartbeat(heartbeat):
    logging.info("Thread %s: starting", heartbeat)
    while(1):
        GPIO.output(htbt, GPIO.HIGH)
        time.sleep(interval)
        GPIO.output(htbt, GPIO.LOW)
        time.sleep(interval)


# Send MAVLink message 
def thread_transmit(transmit):
    msg = "GCS to Drone"
    logging.info("Thread %s: starting", transmit)
    """ MAVLink transmission here """
    logging.info("Thread %s: finishing", transmit)

# The main() will create & start the threads
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H: %M: %S")
    
    logging.info("Main : Establish heartbeat connection")
    h = threading.Thread(target=thread_heartbeat, args=(1,)) # Create thread
    h.start()   # Start thread
    logging.info("Main : Heartbeat established")

    logging.info("Main : Establish transmission channel")
    t = threading.Thread(target=thread_transmit, args=(1,)) # Create thread
    t.start()   # Start thread

    

