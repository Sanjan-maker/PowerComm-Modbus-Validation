
import csv
import os
from datetime import datetime


# Project root directory
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

LOG_FILE = os.path.join(
    BASE_DIR,
    "data",
    "protocol_test_results.csv"
)


class ProtocolLogger:
    """
    Stores protocol validation and test results
    in CSV format.

    Educational industrial-protocol validation prototype.
    """

    HEADERS = [
        "timestamp",
        "test_id",
        "device_ip",
        "port",
        "function",
        "register",
        "expected",
        "actual",
        "status",
        "response_time_ms",
        "error_message",
    ]

    @staticmethod
    def initialize():
        """
        Create the data directory and CSV file
        if they do not already exist.
        """

        os.makedirs(
            os.path.dirname(LOG_FILE),
            exist_ok=True
        )

        if not os.path.exists(LOG_FILE):

            with open(
                LOG_FILE,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow(
                    ProtocolLogger.HEADERS
                )

    @staticmethod
    def log_result(
        test_id,
        device_ip,
        port,
        function,
        register,
        expected,
        actual,
        status,
        response_time_ms=None,
        error_message=None,
    ):
        """
        Append one protocol test result to the CSV log.
        """

        ProtocolLogger.initialize()

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(
            LOG_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                timestamp,
                test_id,
                device_ip,
                port,
                function,
                register,
                expected,
                actual,
                status,
                response_time_ms,
                error_message,
            ])

    @staticmethod
    def show_last_results(count=10):
        """
        Display the most recent protocol test results.
        """

        ProtocolLogger.initialize()

        with open(
            LOG_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            rows = list(
                csv.DictReader(file)
            )

        print()
        print("=" * 80)
        print("RECENT PROTOCOL TEST RESULTS")
        print("=" * 80)

        if not rows:

            print("No test results available.")
            return

        for row in rows[-count:]:

            print()
            print(
                f'{row["timestamp"]} | '
                f'{row["test_id"]} | '
                f'{row["status"]}'
            )

            print(
                f'Function : {row["function"]}'
            )

            print(
                f'Register : {row["register"]}'
            )

            print(
                f'Expected : {row["expected"]}'
            )

            print(
                f'Actual   : {row["actual"]}'
            )

            print(
                f'Response : '
                f'{row["response_time_ms"]} ms'
            )

            if row["error_message"]:

                print(
                    f'Error    : '
                    f'{row["error_message"]}'
                )

    @staticmethod
    def get_all_results():
        """
        Return all logged test results as a list
        of dictionaries.

        Used by the reporting module.
        """

        ProtocolLogger.initialize()

        with open(
            LOG_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            return list(
                csv.DictReader(file)
            )


if __name__ == "__main__":

    ProtocolLogger.initialize()

    print("=" * 60)
    print("PROTOCOLTEST - LOGGER")
    print("=" * 60)

    print()
    print(f"Log file: {LOG_FILE}")

    print()
    print("Logger initialized successfully.")

    print()
    print(
        f"Existing results: "
        f"{len(ProtocolLogger.get_all_results())}"
    )

