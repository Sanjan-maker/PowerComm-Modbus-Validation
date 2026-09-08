
from pymodbus.client import ModbusTcpClient


class FaultInjector:
    """
    Controlled fault-injection utilities for the
    ProtocolTest educational validation prototype.
    """

    @staticmethod
    def explain_modbus_exception(response):
        """
        Convert a Modbus exception code into a
        human-readable diagnostic message.
        """

        exception_code = getattr(
            response,
            "exception_code",
            None
        )

        meanings = {
            1: "Illegal Function",
            2: "Illegal Data Address",
            3: "Illegal Data Value",
            4: "Server Device Failure",
            5: "Acknowledge",
            6: "Server Device Busy",
        }

        meaning = meanings.get(
            exception_code,
            "Unknown Modbus Exception"
        )

        print(f"Exception Code : {exception_code:02d}")
        print(f"Meaning        : {meaning}")

        return meaning

    @staticmethod
    def test_wrong_port(
        host="127.0.0.1",
        port=5999
    ):
        """
        Test communication using an unavailable TCP port.
        """

        print("=" * 60)
        print("FAULT SCENARIO : WRONG TCP PORT")
        print("=" * 60)

        print(f"Device : {host}:{port}")

        client = ModbusTcpClient(
            host=host,
            port=port,
            timeout=2
        )

        try:

            connected = client.connect()

            if connected:

                print()
                print("RESULT")
                print("-" * 40)
                print("Status : UNEXPECTED CONNECTION")

                return False

            print()
            print("RESULT")
            print("-" * 40)
            print("Status : CONNECTION FAILED")

            print()
            print("TROUBLESHOOTING")
            print("-" * 40)
            print("1. Verify device availability")
            print("2. Verify IP address")
            print("3. Verify TCP port")
            print("4. Verify network connectivity")

            return True

        except Exception as error:

            print()
            print("RESULT")
            print("-" * 40)
            print("Status : CONNECTION ERROR")
            print(f"Error  : {error}")

            print()
            print("TROUBLESHOOTING")
            print("-" * 40)
            print("1. Verify device availability")
            print("2. Verify IP address")
            print("3. Verify TCP port")
            print("4. Verify network connectivity")

            return True

        finally:

            client.close()

    @staticmethod
    def test_invalid_register(
        host="127.0.0.1",
        port=5020,
        device_id=1
    ):
        """
        Request a register outside the defined
        electrical device register map.
        """

        print()
        print("=" * 60)
        print("FAULT SCENARIO : INVALID REGISTER")
        print("=" * 60)

        print(f"Device   : {host}:{port}")
        print("Register : 5000")

        client = ModbusTcpClient(
            host=host,
            port=port,
            timeout=3
        )

        try:

            if not client.connect():

                print()
                print("RESULT")
                print("-" * 40)
                print("Status : CONNECTION FAILED")

                return False

            response = client.read_input_registers(
                address=5000,
                count=1,
                device_id=device_id
            )

            print()
            print("RESULT")
            print("-" * 40)

            if response.isError():

                print("Status : PROTOCOL ERROR DETECTED")

                print()
                FaultInjector.explain_modbus_exception(
                    response
                )

                print()
                print(f"Raw Response : {response}")

                print()
                print("TROUBLESHOOTING")
                print("-" * 40)
                print("1. Verify register address")
                print("2. Check device register map")
                print("3. Verify function code")
                print("4. Verify device configuration")

                return True

            print("Status : UNEXPECTED VALID RESPONSE")
            print("Warning: Device accepted the request.")

            return False

        except Exception as error:

            print()
            print("RESULT")
            print("-" * 40)
            print("Status : COMMUNICATION ERROR")
            print(f"Error  : {error}")

            return True

        finally:

            client.close()

    @staticmethod
    def test_invalid_device_id(
        host="127.0.0.1",
        port=5020
    ):
        """
        Attempt communication using an invalid
        Modbus Unit ID.
        """

        invalid_device_id = 99

        print()
        print("=" * 60)
        print("FAULT SCENARIO : INVALID UNIT ID")
        print("=" * 60)

        print(f"Device ID : {invalid_device_id}")

        client = ModbusTcpClient(
            host=host,
            port=port,
            timeout=3
        )

        try:

            if not client.connect():

                print()
                print("RESULT")
                print("-" * 40)
                print("Status : CONNECTION FAILED")

                return False

            response = client.read_input_registers(
                address=1000,
                count=5,
                device_id=invalid_device_id
            )

            print()
            print("RESULT")
            print("-" * 40)

            if response.isError():

                print("Status : PROTOCOL ERROR DETECTED")

                print()
                FaultInjector.explain_modbus_exception(
                    response
                )

                print()
                print(f"Raw Response : {response}")

                print()
                print("TROUBLESHOOTING")
                print("-" * 40)
                print("1. Verify Modbus Unit ID")
                print("2. Verify device configuration")
                print("3. Check network device mapping")

                return True

            print("Status : UNEXPECTED VALID RESPONSE")

            return False

        except Exception as error:

            print()
            print("RESULT")
            print("-" * 40)
            print("Status : COMMUNICATION ERROR")
            print(f"Error  : {error}")

            return True

        finally:

            client.close()


def main():

    print()
    print("=" * 60)
    print("PROTOCOLTEST - FAULT INJECTION")
    print("=" * 60)

    print()
    print("[1] Testing wrong TCP port...")

    FaultInjector.test_wrong_port()

    print()
    print("[2] Testing invalid register...")

    FaultInjector.test_invalid_register()

    print()
    print("[3] Testing invalid Unit ID...")

    FaultInjector.test_invalid_device_id()

    print()
    print("=" * 60)
    print("FAULT INJECTION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":

    main()

