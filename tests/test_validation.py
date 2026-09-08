from validation.validation_engine import ValidationEngine


def test_voltage_within_valid_range():

    result = ValidationEngine.validate_range(
        test_id="TC-REG-001",
        test_name="Read Voltage Register",
        value=229.4,
        minimum=200,
        maximum=250,
        unit="V"
    )

    assert result.status == "PASS"


def test_voltage_below_valid_range():

    result = ValidationEngine.validate_range(
        test_id="TC-BND-001",
        test_name="Voltage Lower Boundary",
        value=180,
        minimum=200,
        maximum=250,
        unit="V"
    )

    assert result.status == "FAIL"


def test_voltage_above_valid_range():

    result = ValidationEngine.validate_range(
        test_id="TC-BND-002",
        test_name="Voltage Upper Boundary",
        value=270,
        minimum=200,
        maximum=250,
        unit="V"
    )

    assert result.status == "FAIL"