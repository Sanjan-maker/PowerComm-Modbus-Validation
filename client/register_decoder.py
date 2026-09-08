REGISTER_MAP = {
    1000: {
        "name": "Voltage",
        "unit": "V",
        "scale": 10,
    },
    1001: {
        "name": "Current",
        "unit": "A",
        "scale": 100,
    },
    1002: {
        "name": "Frequency",
        "unit": "Hz",
        "scale": 100,
    },
    1003: {
        "name": "Power Factor",
        "unit": "",
        "scale": 1000,
    },
    1004: {
        "name": "Active Power",
        "unit": "W",
        "scale": 10,
    },
}


def decode_register(address, raw_value):
    """
    Convert a raw Modbus register into an engineering value.
    """

    if address not in REGISTER_MAP:
        raise ValueError(
            f"Unknown register address: {address}"
        )

    definition = REGISTER_MAP[address]

    engineering_value = (
        raw_value / definition["scale"]
    )

    return {
        "address": address,
        "name": definition["name"],
        "raw_value": raw_value,
        "engineering_value": engineering_value,
        "unit": definition["unit"],
    }


def decode_registers(registers, start_address=1000):
    """
    Decode a sequence of Modbus registers.
    """

    decoded = []

    for index, raw_value in enumerate(registers):

        address = start_address + index

        decoded.append(
            decode_register(
                address,
                raw_value
            )
        )

    return decoded


if __name__ == "__main__":

    test_data = [
        2305,
        1000,
        5000,
        920,
        21160,
    ]

    results = decode_registers(test_data)

    print("=" * 50)
    print("REGISTER DECODER TEST")
    print("=" * 50)

    for result in results:

        unit = result["unit"]

        print(
            f'{result["address"]}: '
            f'{result["name"]} = '
            f'{result["engineering_value"]} '
            f'{unit} '
            f'(RAW: {result["raw_value"]})'
        )