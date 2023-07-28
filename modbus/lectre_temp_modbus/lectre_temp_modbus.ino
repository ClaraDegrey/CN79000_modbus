//lecture de temperature
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
uint16_t value = 0; // Declare and initialize the value variable
if (!ModbusRTUClient.requestFrom(1, HOLDING_REGISTERS, 0, 1)) {
Serial.print("Failed to read value! Error: ");
Serial.println(ModbusRTUClient.lastError());
} else {
value = ModbusRTUClient . holdingRegisterRead (1 ,0);
}

Serial.println(value);
}
