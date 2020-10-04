/* Author: jlicari, AVN, Helium Aero
   Date: 3 October 2020
   Sends UART sample data 
 */
 
#define MAX_INDEX 255
#define CONNECT_TIME 1000

byte *msg_ptr;
int byte_index, ctr;

void setup() {

  byte msg[MAX_INDEX+1];  // 256 Byte array
  msg_ptr = &msg[0];      // Stores address of array
  byte_index = 0;         // Index of array
  ctr = 0;

  Serial.begin(115200);
}

void loop() { 
  // Set sample data
  for (ctr=0; ctr<MAX_INDEX; ctr++) {
    *(msg_ptr+ctr) = ctr+10;
    byte_index = ctr;
  }
  // Send sample data
  for (ctr=0; ctr<byte_index; ctr++) {
    Serial.write(*(msg_ptr+ctr)); // Write to UART
    *(msg_ptr+ctr) = 0; // Clear buffer
  }
  byte_index = 0;
}
