# Communication Flow

- LinkManager always has a UDP link open waiting for a Vehicle heartbeat

- LinkManager detects a new known device (Pixhawk, SiK Radio, PX4 Flow) connected to computer
    - Creates a new SerialLink connected to the device
- Bytes comes through Link and are sent to MAVLinkProtocol
- MAVLinkProtocol converts the bytes into a MAVLink message
- If the message is a HEARTBEAT the MultiVehicleManager is notified
- MultiVehicleManager is notifed of the HEARTBEAT and creates a new Vehicle object based on the information in the HEARTBEAT message
- The Vehicle instantiates the plugins which match the vehicle type
- The ParameterLoader associated with the vehicle sends a PARAM_REQUEST_LIST to the vehicle to load params using the parameter protocol
- Once parameter load is complete, the MissionManager associated with the Vehicle requests the mission items from the Vehicle using the mission item protocol
- Once parameter load is complete, the VehicleComponents display their UI in the Setup view

# Using mavutil
Most developers will use the mavutil module to set up and manage the communication channel (because it makes get started very easy). This module provides simple mechanisms for setting up links, sending and receiving messages, and querying some basic autopilot properties (e.g. flight mode). It provides access to the dialect module used for encoding/decoding/signing via an attribute (mav).

There are several main caveats to be aware of when using mavutil:

- The link does not properly handle multiple systems running on the same port. If you need a multi-vehicle network see source-system-filtering.
- The module is optimised for ArduPilot and some functions may not work properly on other autopilots.
- mavutil is still a relatively low-level MAVLink API. It has limited support for even the most common MAVLink microservices.