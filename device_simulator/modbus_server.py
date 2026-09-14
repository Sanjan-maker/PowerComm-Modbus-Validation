import time
import threading

from pymodbus.simulator import SimData, SimDevice
from pymodbus.simulator.simdata import DataType
from pymodbus.server import StartTcpServer

from device_simulator.electrical_device import ElectricalDevice


HOST = "127.0.0.1"
PORT = 5020
DEVICE_ID = 1

START_ADDRESS = 1000
REGISTER_COUNT = 5


class ProtocolTestServer:

    def __init__(self):

      
        # ELECTRICAL DEVICE SIMULATION
       
        self.electrical_device = ElectricalDevice()

      
        # INPUT REGISTERS
    
    
        # 1000 -> Voltage
        # 1001 -> Current
        # 1002 -> Frequency
        # 1003 -> Power Factor
        # 1004 -> Active Power
        

        self.input_registers = SimData(
            address=START_ADDRESS,
            count=REGISTER_COUNT,
            values=[
                2305,
                1000,
                5000,
                920,
                21160
            ],
            datatype=DataType.REGISTERS,
            readonly=True,
        )

       
        
        # Coil 1 -> Breaker Command
        
       
        self.coils = SimData(
            address=1,
            count=1,
            values=[0],
            datatype=DataType.BITS,
            readonly=False,
        )

      
        # Discrete Input 1 -> Breaker Status
       

        self.discrete_inputs = SimData(
            address=1,
            count=1,
            values=[0],
            datatype=DataType.BITS,
            readonly=True,
        )

      
        # HOLDING REGISTERS
        

        self.holding_registers = SimData(
            address=1,
            count=10,
            values=[0] * 10,
            datatype=DataType.REGISTERS,
            readonly=False,
        )

       
        # MODBUS DEVICE
     
        self.device = SimDevice(
            id=DEVICE_ID,
            simdata=(
                [self.discrete_inputs],
                [self.coils],
                [self.holding_registers],
                [self.input_registers],
            ),
        )

      
        # THREAD CONTROL
       

        self.running = True

        self.lock = threading.Lock()

    
    # ENCODE ENGINEERING VALUES
    
   

    def encode_measurements(self):

        measurements = (
            self.electrical_device.get_measurements()
        )

        
        # Engineering value:
        #     230.5 V
        
        

        voltage = int(
            round(
                measurements["voltage"] * 10
            )
        )

       

        current = int(
            round(
                measurements["current"] * 100
            )
        )

       
        frequency = int(
            round(
                measurements["frequency"] * 100
            )
        )

        

        power_factor = int(
            round(
                measurements["power_factor"] * 1000
            )
        )

        

        active_power = int(
            round(
                measurements["active_power"] * 10
            )
        )

        return [
            voltage,
            current,
            frequency,
            power_factor,
            active_power,
        ]

   
    def update_device_data(self):

        with self.lock:

           

            self.electrical_device.update_measurements()

           

            raw_values = self.encode_measurements()

           

            for index, value in enumerate(raw_values):

                self.input_registers.values[index] = value

            

            breaker_status = (
                self.electrical_device.breaker_status
            )

            self.discrete_inputs.values[0] = (
                1 if breaker_status else 0
            )

   

    def simulation_loop(self):

        print()
        print("Continuous simulation started.")
        print("Update interval : 1 second")
        print()

        while self.running:

            try:

                self.update_device_data()


                measurements = (
                    self.electrical_device
                    .get_measurements()
                )

                print(
                    f"[SIMULATION] "
                    f"Voltage={measurements['voltage']:.2f} V | "
                    f"Current={measurements['current']:.2f} A | "
                    f"Frequency={measurements['frequency']:.2f} Hz | "
                    f"PF={measurements['power_factor']:.3f} | "
                    f"Power={measurements['active_power']:.2f} W"
                )

                time.sleep(1)

            except Exception as error:

                print(
                    f"[SIMULATION ERROR] {error}"
                )

                time.sleep(1)

   
    def start(self):

        print("=" * 60)
        print("PROTOCOLTEST - MODBUS TCP SERVER")
        print("=" * 60)

        print()
        print(f"Host      : {HOST}")
        print(f"Port      : {PORT}")
        print(f"Device ID : {DEVICE_ID}")

        print()
        print("Dynamic electrical simulation enabled.")

       
        print()
        print("INPUT REGISTERS")
        print("-" * 40)

        print("1000 -> Voltage")
        print("1001 -> Current")
        print("1002 -> Frequency")
        print("1003 -> Power Factor")
        print("1004 -> Active Power")

        print()
        print("COILS")
        print("-" * 40)

        print("1 -> Breaker Command")

        print()
        print("DISCRETE INPUTS")
        print("-" * 40)

        print("1 -> Breaker Status")

       
        print()
        print("Initializing electrical measurements...")

        self.update_device_data()

      
        simulation_thread = threading.Thread(
            target=self.simulation_loop,
            daemon=True,
            name="ElectricalSimulation"
        )

        simulation_thread.start()

        print()
        print("Simulation loop running every 1 second.")
        print("Waiting for Modbus TCP clients...")
        print("Press CTRL+C to stop.")
        print()

       

        StartTcpServer(
            context=self.device,
            address=(HOST, PORT),
        )

  
    def stop(self):

        self.running = False

        print()
        print("Simulation stopped.")



if __name__ == "__main__":

    server = ProtocolTestServer()

    try:

        server.start()

    except KeyboardInterrupt:

        server.stop()

        print(
            "Server stopped."
        )
