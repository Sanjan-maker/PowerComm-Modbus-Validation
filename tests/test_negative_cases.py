

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


def test_invalid_register_address():

    """
    Negative test:
    Request a register outside the defined
    electrical measurement map.
    """

    client = create_client()

    try:

        assert client.connect() is True

        response = client.read_input_registers(
            address=5000,
            count=1,
            device_id=DEVICE_ID
        )

        assert response.isError() is True

    finally:

        client.close()


def test_register_response_length():

    """
    Protocol/application validation test:
    Request multiple registers and verify that
    the returned response is handled correctly.
    """

    client = create_client()

    try:

        assert client.connect() is True

        response = client.read_input_registers(
            address=1000,
            count=20,
            device_id=DEVICE_ID
        )

        assert response.isError() is False

        # The simulator may return additional register
        # locations, so we verify that a response was received
        # rather than incorrectly treating the request itself
        # as a Modbus protocol error.

        assert len(response.registers) == 20

    finally:

        client.close()


def test_invalid_device_id():

    """
    Negative test:
    Communicate using an incorrect Modbus Unit ID.
    """

    client = create_client()

    try:

        assert client.connect() is True

        response = client.read_input_registers(
            address=1000,
            count=5,
            device_id=99
        )

        assert response.isError() is True

    finally:

        client.close()


def test_connection_to_wrong_port():

    """
    Negative test:
    Attempt communication with an unavailable
    TCP port.
    """

    client = ModbusTcpClient(
        host=HOST,
        port=5999,
        timeout=1
    )

    try:

        connected = client.connect()

        assert connected is False

    finally:

        client.close()

