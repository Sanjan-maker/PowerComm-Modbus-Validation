
import time

from pymodbus.client import ModbusTcpClient


HOST = "127.0.0.1"
PORT = 5020
DEVICE_ID = 1

TOTAL_REQUESTS = 100


def run_performance_test():

    print("=" * 60)
    print("PROTOCOLTEST - MODBUS TCP PERFORMANCE TEST")
    print("=" * 60)

    print()
    print(f"Device         : {HOST}:{PORT}")
    print(f"Unit ID        : {DEVICE_ID}")
    print(f"Total Requests : {TOTAL_REQUESTS}")

    client = ModbusTcpClient(
        host=HOST,
        port=PORT,
        timeout=3
    )

    print()
    print("Connecting to device...")

    if not client.connect():

        print("CONNECTION FAILED")
        return

    print("CONNECTED")

    successful_requests = 0
    failed_requests = 0

    response_times = []

    print()
    print("Executing requests...")
    print("-" * 60)

    total_start = time.perf_counter()

    for request_number in range(1, TOTAL_REQUESTS + 1):

        request_start = time.perf_counter()

        try:

            response = client.read_input_registers(
                address=1000,
                count=5,
                device_id=DEVICE_ID
            )

            request_end = time.perf_counter()

            response_time_ms = (
                request_end - request_start
            ) * 1000

            if response.isError():

                failed_requests += 1

            else:

                successful_requests += 1
                response_times.append(
                    response_time_ms
                )

        except Exception:

            failed_requests += 1

    total_end = time.perf_counter()

    client.close()

    total_time_ms = (
        total_end - total_start
    ) * 1000

    if response_times:

        average_response_time = (
            sum(response_times)
            / len(response_times)
        )

        minimum_response_time = min(
            response_times
        )

        maximum_response_time = max(
            response_times
        )

    else:

        average_response_time = 0
        minimum_response_time = 0
        maximum_response_time = 0

    success_rate = (
        successful_requests
        / TOTAL_REQUESTS
    ) * 100

    print()
    print("=" * 60)
    print("PERFORMANCE TEST REPORT")
    print("=" * 60)

    print()
    print(f"Total Requests          : {TOTAL_REQUESTS}")
    print(f"Successful Requests     : {successful_requests}")
    print(f"Failed Requests         : {failed_requests}")

    print()
    print(f"Success Rate            : {success_rate:.2f}%")

    print()
    print(
        f"Total Execution Time    : "
        f"{total_time_ms:.2f} ms"
    )

    print(
        f"Average Response Time   : "
        f"{average_response_time:.2f} ms"
    )

    print(
        f"Minimum Response Time   : "
        f"{minimum_response_time:.2f} ms"
    )

    print(
        f"Maximum Response Time   : "
        f"{maximum_response_time:.2f} ms"
    )

    print()
    print("=" * 60)
    print("PERFORMANCE TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":

    run_performance_test()

