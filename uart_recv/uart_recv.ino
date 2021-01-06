/* Author: jlicari, AVN, Helium Aero
   Date: 3 October 2020
   Receives UART data and displays it on Serial Monitor
 */
 
#define MAX_INDEX 8
#define CONNECT_TIME 1000

byte *msg_ptr;
int byte_index, ctr, time1, time2;

void setup() {

  byte msg[MAX_INDEX];    // 8 Byte array
  msg_ptr = &msg[0];      // Stores address of array
  byte_index = 0;         // Index of array
  time1 = 0;
  time2 = 0;
  ctr = 0;
 
  Serial.begin(9600);
  Serial.println("--- UART RECEIVER ---");
}

void loop() { 
  // Receive and store data
  if (Serial.available()) { // Check if Serial port is available
    
    // Allow time for connection (use delay() if single thread
    time1 = millis();
    while ((time1+time2) < CONNECT_TIME) {
      time2 = millis();
    }
    
    while(Serial.available()) { // If data is being passed on the channel
      *(msg_ptr+byte_index) = Serial.read(); // Store 1 byte into array index 
      byte_index++; // Increment the array index
    }
  }
  // Print and clear buffer
  for (ctr = 0; ctr < byte_index; ctr++) {
     Serial.print("Byte ");
     Serial.print(ctr);
     Serial.print(": ");
     Serial.print(*(msg_ptr+ctr));  // Print each byte
     Serial.println("\n"); 
     *(msg_ptr+ctr) = 0;  // Clear buffer
  }
  byte_index = 0; // Reset the byte index
}
