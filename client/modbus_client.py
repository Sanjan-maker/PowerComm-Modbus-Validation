import time

from pymodbus.client import ModbusTcpClient

from client.register_decoder import decode_registers
from validation.validation_engine import ValidationEngine
from logger.protocol_logger import ProtocolLogger


HOST = "127.0.0.1"
PORT = 5020
DEVICE_ID = 1

START_ADDRESS = 1000
REGISTER_COUNT = 5


class ModbusElectricalClient:

    def __init__(
        self,
        host=HOST,
        port=PORT,
        device_id=DEVICE_ID
    ):

        self.host = host
        self.port = port
        self.device_id = device_id

        self.client = ModbusTcpClient(
            host=self.host,
            port=self.port,
            timeout=3
        )

        self.connected = False

    # ==================================================
    # CONNECT
    # ==================================================

    def connect(self):

        if self.connected and self.client.connected:
            return True

        try:

            connected = self.client.connect()

            if connected:

                self.connected = True

                print(
                    f"CONNECTED -> "
                    f"{self.host}:{self.port}"
                )

                return True

            print("CONNECTION FAILED")

            self.connected = False

            return False

        except Exception as error:

            print(
                f"Connection error: {error}"
            )

            self.connected = False

            return False

    # ==================================================
    # DISCONNECT
    # ==================================================

    def disconnect(self):

        if self.client:

            self.client.close()

        if self.connected:

            print("Disconnected from device.")

        self.connected = False

    # ==================================================
    # READ INPUT REGISTERS
    # ==================================================

    def read_input_registers(self):

        if not self.connected:

            if not self.connect():

                return None, 0

        start_time = time.perf_counter()

        try:

            response = (
                self.client.read_input_registers(
                    address=START_ADDRESS,
                    count=REGISTER_COUNT,
                    device_id=self.device_id
                )
            )

            response_time_ms = (
                time.perf_counter() - start_time
            ) * 1000

            # --------------------------------------------------
            # MODBUS ERROR
            # --------------------------------------------------

            if response.isError():

                print(
                    "Modbus error received:"
                )

                print(response)

                return (
                    None,
                    response_time_ms
                )

            # --------------------------------------------------
            # CHECK REGISTER COUNT
            # --------------------------------------------------

            if (
                not hasattr(response, "registers")
                or
                len(response.registers)
                != REGISTER_COUNT
            ):

                print(
                    "Invalid register response length:"
                    f" {len(response.registers)}"
                )

                return (
                    None,
                    response_time_ms
                )

            return (
                response.registers,
                response_time_ms
            )

        except Exception as error:

            response_time_ms = (
                time.perf_counter() - start_time
            ) * 1000

            print(
                f"Communication error: {error}"
            )

            self.connected = False

            return (
                None,
                response_time_ms
            )

    # ==================================================
    # DECODE
    # ==================================================

    def decode(self, registers):

        return decode_registers(
            registers,
            start_address=START_ADDRESS
        )

    # ==================================================
    # VALIDATE VOLTAGE
    # ==================================================

    def validate_voltage(
        self,
        decoded_values
    ):

        voltage = decoded_values[0][
            "engineering_value"
        ]

        return ValidationEngine.validate_range(
            test_id="TC-REG-001",
            test_name="Read Voltage Register",
            value=voltage,
            minimum=200,
            maximum=250,
            unit="V"
        )

    # ==================================================
    # VALIDATE CURRENT
    # ==================================================

    def validate_current(
        self,
        decoded_values
    ):

        current = decoded_values[1][
            "engineering_value"
        ]

        return ValidationEngine.validate_range(
            test_id="TC-REG-002",
            test_name="Read Current Register",
            value=current,
            minimum=0,
            maximum=100,
            unit="A"
        )

    # ==================================================
    # VALIDATE FREQUENCY
    # ==================================================

    def validate_frequency(
        self,
        decoded_values
    ):

        frequency = decoded_values[2][
            "engineering_value"
        ]

        return ValidationEngine.validate_range(
            test_id="TC-REG-003",
            test_name="Read Frequency Register",
            value=frequency,
            minimum=49,
            maximum=51,
            unit="Hz"
        )

    # ==================================================
    # VALIDATE POWER FACTOR
    # ==================================================

    def validate_power_factor(
        self,
        decoded_values
    ):

        power_factor = decoded_values[3][
            "engineering_value"
        ]

        return ValidationEngine.validate_range(
            test_id="TC-REG-004",
            test_name="Read Power Factor Register",
            value=power_factor,
            minimum=0,
            maximum=1,
            unit=""
        )

    # ==================================================
    # VALIDATE ACTIVE POWER
    # ==================================================

    def validate_active_power(
        self,
        decoded_values
    ):

        active_power = decoded_values[4][
            "engineering_value"
        ]

        return ValidationEngine.validate_range(
            test_id="TC-REG-005",
            test_name="Read Active Power Register",
            value=active_power,
            minimum=0,
            maximum=10000,
            unit="W"
        )

    # ==================================================
    # RUN VALIDATION
    # ==================================================

    def run_register_validation(
        self,
        decoded_values
    ):

        results = []

        results.append(
            self.validate_voltage(
                decoded_values
            )
        )

        results.append(
            self.validate_current(
                decoded_values
            )
        )

        results.append(
            self.validate_frequency(
                decoded_values
            )
        )

        results.append(
            self.validate_power_factor(
                decoded_values
            )
        )

        results.append(
            self.validate_active_power(
                decoded_values
            )
        )

        return results

    # ==================================================
    # LOG RESULTS
    # ==================================================

    def log_results(
        self,
        results,
        response_time_ms
    ):

        for index, result in enumerate(results):

            register_address = (
                START_ADDRESS + index
            )

            ProtocolLogger.log_result(
                test_id=result.test_id,
                device_ip=self.host,
                port=self.port,
                function="Read Input Registers",
                register=register_address,
                expected=result.expected,
                actual=result.actual,
                status=result.status,
                response_time_ms=round(
                    response_time_ms,
                    3
                ),
                error_message=result.error_message
            )

    # ==================================================
    # READ + DECODE + VALIDATE
    # ==================================================

    def read_and_validate(self):

        registers, response_time_ms = (
            self.read_input_registers()
        )

        if registers is None:

            return {
                "success": False,
                "registers": None,
                "decoded": None,
                "results": [],
                "response_time_ms":
                    response_time_ms,
            }

        decoded_values = self.decode(
            registers
        )

        results = self.run_register_validation(
            decoded_values
        )

        self.log_results(
            results,
            response_time_ms
        )

        return {
            "success": True,
            "registers": registers,
            "decoded": decoded_values,
            "results": results,
            "response_time_ms":
                response_time_ms,
        }

    # ==================================================
    # CONTINUOUS MONITORING
    # ==================================================

    def monitor(
        self,
        interval=1
    ):

        if not self.connect():

            return

        print()
        print("=" * 60)
        print("CONTINUOUS MODBUS MONITORING")
        print("=" * 60)

        print()
        print("Press CTRL+C to stop.")
        print()

        try:

            while True:

                data = self.read_and_validate()

                if not data["success"]:

                    print(
                        "Unable to read device."
                    )

                    time.sleep(interval)

                    continue

                decoded = data["decoded"]

                response_time = data[
                    "response_time_ms"
                ]

                print()
                print(
                    "-" * 60
                )

                for item in decoded:

                    print(
                        f'{item["name"]:<15}: '
                        f'{item["engineering_value"]} '
                        f'{item["unit"]}'
                    )

                print(
                    f"Response Time  : "
                    f"{response_time:.3f} ms"
                )

                passed = sum(
                    1
                    for result in data["results"]
                    if result.status == "PASS"
                )

                failed = len(
                    data["results"]
                ) - passed

                print(
                    f"Validation     : "
                    f"{passed} PASS / "
                    f"{failed} FAIL"
                )

                time.sleep(interval)

        except KeyboardInterrupt:

            print()
            print(
                "Monitoring stopped."
            )

        finally:

            self.disconnect()


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)
    print("PROTOCOLTEST - MODBUS TCP CLIENT")
    print("=" * 60)

    print()
    print(f"Device : {HOST}:{PORT}")
    print(f"Unit ID: {DEVICE_ID}")
    print()

    client = ModbusElectricalClient()

    # Continuous monitoring
    client.monitor(interval=1)


if __name__ == "__main__":

    main()