//modification de l unite de tempeature
#include <ArduinoRS485.h>
#include <ArduinoModbus.h>

void setup() {
Serial.begin(9600);
if (!ModbusRTUClient.begin(9600,SERIAL_8N1)) {
Serial.println("Failed to start Modbus RTU Client!");
while (1);
}
}

void loop() {
uint16_t value = 10; // Declare and initialize the value variable

ModbusRTUClient.beginTransmission(1, HOLDING_REGISTERS, 51, 1);
ModbusRTUClient.write(0); 
if (!ModbusRTUClient.endTransmission()) {
Serial.print("failed! ");
Serial.println(ModbusRTUClient.lastError());
} else {
Serial.println("success");
}
value=ModbusRTUClient.holdingRegisterRead(1,51);

Serial.println(value);
}
