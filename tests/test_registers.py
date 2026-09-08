
from pymodbus.client import ModbusTcpClient


HOST = "127.0.0.1"
PORT = 5020
DEVICE_ID = 1


def create_client():

    return ModbusTcpClient(
        host=HOST,
        port=PORT,
        timeout=3
    )


def test_modbus_connection():

    client = create_client()

    try:

        connected = client.connect()

        assert connected is True

    finally:

        client.close()


def test_read_electrical_registers():

    client = create_client()

    try:

        assert client.connect() is True

        response = client.read_input_registers(
            address=1000,
            count=5,
            device_id=DEVICE_ID
        )

        assert response.isError() is False
        assert len(response.registers) == 5

    finally:

        client.close()


def test_voltage_register():

    client = create_client()

    try:

        assert client.connect() is True

        response = client.read_input_registers(
            address=1000,
            count=1,
            device_id=DEVICE_ID
        )

        assert response.isError() is False

        raw_voltage = response.registers[0]

        voltage = raw_voltage / 10

        assert 200 <= voltage <= 250

    finally:

        client.close()


def test_frequency_register():

    client = create_client()

    try:

        assert client.connect() is True

        response = client.read_input_registers(
            address=1002,
            count=1,
            device_id=DEVICE_ID
        )

        assert response.isError() is False

        raw_frequency = response.registers[0]

        frequency = raw_frequency / 100

        assert 49 <= frequency <= 51

    finally:

        client.close()


def test_power_factor_register():

    client = create_client()

    try:

        assert client.connect() is True

        response = client.read_input_registers(
            address=1003,
            count=1,
            device_id=DEVICE_ID
        )

        assert response.isError() is False

        raw_power_factor = response.registers[0]

        power_factor = raw_power_factor / 1000

        assert 0 <= power_factor <= 1

    finally:

        client.close()

