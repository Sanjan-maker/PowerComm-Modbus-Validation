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

        # ==================================================
        # ELECTRICAL DEVICE SIMULATION
        # ==================================================

        self.electrical_device = ElectricalDevice()

        # ==================================================
        # INPUT REGISTERS
        # ==================================================
        #
        # 1000 -> Voltage
        # 1001 -> Current
        # 1002 -> Frequency
        # 1003 -> Power Factor
        # 1004 -> Active Power
        #
        # These values will be continuously updated.
        # ==================================================

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

        # ==================================================
        # COILS
        # ==================================================
        #
        # Coil 1 -> Breaker Command
        #
        # IMPORTANT:
        # Use a list for BITS data.
        # ==================================================

        self.coils = SimData(
            address=1,
            count=1,
            values=[0],
            datatype=DataType.BITS,
            readonly=False,
        )

        # ==================================================
        # DISCRETE INPUTS
        # ==================================================
        #
        # Discrete Input 1 -> Breaker Status
        # ==================================================

        self.discrete_inputs = SimData(
            address=1,
            count=1,
            values=[0],
            datatype=DataType.BITS,
            readonly=True,
        )

        # ==================================================
        # HOLDING REGISTERS
        # ==================================================

        self.holding_registers = SimData(
            address=1,
            count=10,
            values=[0] * 10,
            datatype=DataType.REGISTERS,
            readonly=False,
        )

        # ==================================================
        # MODBUS DEVICE
        # ==================================================

        self.device = SimDevice(
            id=DEVICE_ID,
            simdata=(
                [self.discrete_inputs],
                [self.coils],
                [self.holding_registers],
                [self.input_registers],
            ),
        )

        # ==================================================
        # THREAD CONTROL
        # ==================================================

        self.running = True

        self.lock = threading.Lock()

    # ======================================================
    # ENCODE ENGINEERING VALUES
    # ======================================================

    def encode_measurements(self):

        measurements = (
            self.electrical_device.get_measurements()
        )

        # ----------------------------------------------
        # Voltage
        #
        # Engineering value:
        #     230.5 V
        #
        # Modbus raw value:
        #     2305
        # ----------------------------------------------

        voltage = int(
            round(
                measurements["voltage"] * 10
            )
        )

        # ----------------------------------------------
        # Current
        #
        # Engineering value:
        #     10.00 A
        #
        # Modbus raw value:
        #     1000
        # ----------------------------------------------

        current = int(
            round(
                measurements["current"] * 100
            )
        )

        # ----------------------------------------------
        # Frequency
        #
        # Engineering value:
        #     50.00 Hz
        #
        # Modbus raw value:
        #     5000
        # ----------------------------------------------

        frequency = int(
            round(
                measurements["frequency"] * 100
            )
        )

        # ----------------------------------------------
        # Power Factor
        #
        # Engineering value:
        #     0.920
        #
        # Modbus raw value:
        #     920
        # ----------------------------------------------

        power_factor = int(
            round(
                measurements["power_factor"] * 1000
            )
        )

        # ----------------------------------------------
        # Active Power
        #
        # Engineering value:
        #     2116.0 W
        #
        # Modbus raw value:
        #     21160
        # ----------------------------------------------

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

    # ======================================================
    # UPDATE MODBUS DATA
    # ======================================================

    def update_device_data(self):

        with self.lock:

            # ------------------------------------------
            # UPDATE ELECTRICAL SIMULATION
            # ------------------------------------------

            self.electrical_device.update_measurements()

            # ------------------------------------------
            # GET NEW RAW VALUES
            # ------------------------------------------

            raw_values = self.encode_measurements()

            # ------------------------------------------
            # UPDATE INPUT REGISTERS
            # ------------------------------------------

            for index, value in enumerate(raw_values):

                self.input_registers.values[index] = value

            # ------------------------------------------
            # UPDATE BREAKER STATUS
            # ------------------------------------------

            breaker_status = (
                self.electrical_device.breaker_status
            )

            self.discrete_inputs.values[0] = (
                1 if breaker_status else 0
            )

    # ======================================================
    # CONTINUOUS SIMULATION LOOP
    # ======================================================

    def simulation_loop(self):

        print()
        print("Continuous simulation started.")
        print("Update interval : 1 second")
        print()

        while self.running:

            try:

                self.update_device_data()

                # --------------------------------------
                # DEBUG OUTPUT
                # --------------------------------------

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

    # ======================================================
    # START SERVER
    # ======================================================

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

        # ==================================================
        # REGISTER MAP
        # ==================================================

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

        # ==================================================
        # INITIAL UPDATE
        # ==================================================

        print()
        print("Initializing electrical measurements...")

        self.update_device_data()

        # ==================================================
        # START SIMULATION THREAD
        # ==================================================

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

        # ==================================================
        # START MODBUS TCP SERVER
        # ==================================================

        StartTcpServer(
            context=self.device,
            address=(HOST, PORT),
        )

    # ======================================================
    # STOP SERVER
    # ======================================================

    def stop(self):

        self.running = False

        print()
        print("Simulation stopped.")


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    server = ProtocolTestServer()

    try:

        server.start()

    except KeyboardInterrupt:

        server.stop()

        print(
            "Server stopped."
        )