#include <stdio.h>
#include <modbus.h>
#include <errno.h>
#include <errno.h>

int main(){
	

const int REMOTE_ID = 1;  //numero de l'esclave avec lequel on veut interagir
modbus_t *ctx;
uint16_t tab_reg[1]={42};

ctx = modbus_new_rtu("/dev/ttyACM0", 9600, 'N', 8, 1);
if (ctx == NULL) {
    fprintf(stderr, "Unable to create the libmodbus context\n");
    return -1;
}

if (modbus_connect(ctx) == -1) {
    fprintf(stderr, "Connection failed: %s\n", modbus_strerror(errno));
    modbus_free(ctx);
    return -1;
}

modbus_set_slave(ctx, REMOTE_ID);

// Read 2 registers from address 0 of server ID 10.
modbus_read_registers(ctx, 1, 1, tab_reg);  //int modbus_read_registers(modbus_t *ctx, int addr, int nb, uint16_t *dest); (dest=adresse de départ)

printf("%d\n",tab_reg[0]);
return 0;
}
