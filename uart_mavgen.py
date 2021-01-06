#!/usr/bin/python3
import pymavlink
import Jetson.GPIO as GPIO
import threading
import time
import logging
import serial

# Import common module for MAVLink 2
from pymavlink.dialects.v20 import common as mavlink2
from pymavlink import mavutil

# Start a connection listening to a UDP port
drone_connect = mavutil.mavlink_connection('udpin:localhost:14540')

# Wait for the first heartbeat 
#   This sets the system and component ID of remote system for the link
# Create thread for heartbeat (repeats continuously)
# Implemented as daemon: a process that runs in the background
# A program will wait for a thread to complete before it terminates
# A daemon will shut down when the program exits 
# Set the daemon flag during creation in main
def thread_heartbeat(heartbeat):
    logging.info("Daemon %s: starting", heartbeat)
    while(1):
        drone_connect.wait_heartbeat()
        print("Heartbeat from system (system %u component %u)" % (drone_connect.target_system, drone_connect.target_system))

# Once connected, use 'drone_connect' to get and send messages
# Get message


# Request all parameters from drone
# PARAM_REQUEST_LIST

# The main() will create & start the threads
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H: %M: %S")
    
    logging.info("Main : Establish heartbeat connection")
    h = threading.Thread(target=thread_heartbeat, args=(1,), daemon=True) # Create thread
    h.start()   # Start daemon thread
    #logging.info("Main : Heartbeat established")

    logging.info("Main : Establish transmission channel")
    t = threading.Thread(target=thread_transmit, args=(1,)) # Create thread
    t.start()   # Start thread
    t.join()
