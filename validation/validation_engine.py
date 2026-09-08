
from datetime import datetime


class ValidationResult:

    def __init__(
        self,
        test_id,
        test_name,
        expected,
        actual,
        status,
        error_message=None,
        response_time_ms=None,
    ):

        self.test_id = test_id
        self.test_name = test_name
        self.expected = expected
        self.actual = actual
        self.status = status
        self.error_message = error_message
        self.response_time_ms = response_time_ms
        self.timestamp = datetime.now().isoformat()

    def to_dict(self):

        return {
            "timestamp": self.timestamp,
            "test_id": self.test_id,
            "test_name": self.test_name,
            "expected": self.expected,
            "actual": self.actual,
            "status": self.status,
            "error_message": self.error_message,
            "response_time_ms": self.response_time_ms,
        }

    def __repr__(self):

        return (
            f"ValidationResult("
            f"test_id={self.test_id!r}, "
            f"status={self.status!r}, "
            f"actual={self.actual!r})"
        )


class ValidationEngine:

    @staticmethod
    def validate_range(
        test_id,
        test_name,
        value,
        minimum,
        maximum,
        unit="",
    ):

        expected = (
            f"{minimum} <= value <= {maximum} {unit}"
        )

        actual = f"{value} {unit}"

        if minimum <= value <= maximum:

            status = "PASS"

        else:

            status = "FAIL"

        return ValidationResult(
            test_id=test_id,
            test_name=test_name,
            expected=expected,
            actual=actual,
            status=status,
        )

    @staticmethod
    def validate_not_none(
        test_id,
        test_name,
        value,
    ):

        expected = "Valid response"

        if value is not None:

            status = "PASS"
            actual = "Response received"

        else:

            status = "FAIL"
            actual = "No response"

        return ValidationResult(
            test_id=test_id,
            test_name=test_name,
            expected=expected,
            actual=actual,
            status=status,
        )

    @staticmethod
    def validate_register(
        test_id,
        test_name,
        address,
        registers,
    ):

        expected = (
            f"Register {address} available"
        )

        if registers is None:

            return ValidationResult(
                test_id=test_id,
                test_name=test_name,
                expected=expected,
                actual="No response",
                status="FAIL",
            )

        start_address = 1000

        index = address - start_address

        if 0 <= index < len(registers):

            actual = (
                f"Register {address} = "
                f"{registers[index]}"
            )

            status = "PASS"

        else:

            actual = (
                f"Register {address} unavailable"
            )

            status = "FAIL"

        return ValidationResult(
            test_id=test_id,
            test_name=test_name,
            expected=expected,
            actual=actual,
            status=status,
        )


if __name__ == "__main__":

    print("=" * 55)
    print("PROTOCOLTEST - VALIDATION ENGINE TEST")
    print("=" * 55)

    result = ValidationEngine.validate_range(
        test_id="TC-REG-001",
        test_name="Validate Voltage",
        value=229.7,
        minimum=200,
        maximum=250,
        unit="V",
    )

    print()
    print(f"Test ID   : {result.test_id}")
    print(f"Test Name : {result.test_name}")
    print(f"Expected  : {result.expected}")
    print(f"Actual    : {result.actual}")
    print(f"Status    : {result.status}")

