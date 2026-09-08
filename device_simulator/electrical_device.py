import random
import time


class ElectricalDevice:
    """
    Simulates a realistic industrial electrical device.

    The values change smoothly over time instead of jumping
    randomly between completely unrelated values.
    """

    def __init__(self):

        self.voltage = 230.0
        self.current = 10.0
        self.frequency = 50.0
        self.power_factor = 0.92

        self.breaker_status = True

        # Internal simulation time
        self.step = 0

        self.update_measurements()

    # ======================================================
    # UPDATE MEASUREMENTS
    # ======================================================

    def update_measurements(self):

        self.step += 1

        # --------------------------------------------------
        # VOLTAGE
        # --------------------------------------------------

        self.voltage = round(
            230.0
            + random.uniform(-1.5, 1.5),
            1
        )

        # --------------------------------------------------
        # CURRENT
        # --------------------------------------------------

        self.current = round(
            10.0
            + random.uniform(-1.5, 1.5),
            2
        )

        # --------------------------------------------------
        # FREQUENCY
        # --------------------------------------------------

        self.frequency = round(
            50.0
            + random.uniform(-0.15, 0.15),
            2
        )

        # --------------------------------------------------
        # POWER FACTOR
        # --------------------------------------------------

        self.power_factor = round(
            0.94
            + random.uniform(-0.04, 0.04),
            3
        )

        # Keep PF inside realistic range

        self.power_factor = max(
            0.85,
            min(
                self.power_factor,
                0.99
            )
        )

    # ======================================================
    # ACTIVE POWER
    # ======================================================

    def calculate_active_power(self):

        if not self.breaker_status:

            return 0.0

        power = (
            self.voltage
            * self.current
            * self.power_factor
        )

        return round(
            power,
            1
        )

    # ======================================================
    # GET MEASUREMENTS
    # ======================================================

    def get_measurements(self):

        return {

            "voltage":
                self.voltage,

            "current":
                self.current,

            "frequency":
                self.frequency,

            "power_factor":
                self.power_factor,

            "active_power":
                self.calculate_active_power(),

            "breaker_status":
                self.breaker_status,
        }

    # ======================================================
    # BREAKER
    # ======================================================

    def set_breaker(self, state):

        self.breaker_status = bool(state)

    # ======================================================
    # PRINT
    # ======================================================

    def print_measurements(self):

        measurements = (
            self.get_measurements()
        )

        print("=" * 60)

        print(
            f"Voltage      : "
            f"{measurements['voltage']:.1f} V"
        )

        print(
            f"Current      : "
            f"{measurements['current']:.2f} A"
        )

        print(
            f"Frequency    : "
            f"{measurements['frequency']:.2f} Hz"
        )

        print(
            f"Power Factor : "
            f"{measurements['power_factor']:.3f}"
        )

        print(
            f"Active Power : "
            f"{measurements['active_power']:.1f} W"
        )

        print(
            f"Breaker      : "
            f"{'CLOSED' if measurements['breaker_status'] else 'OPEN'}"
        )

        print("=" * 60)


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    device = ElectricalDevice()

    for _ in range(20):

        device.update_measurements()

        device.print_measurements()

        time.sleep(1)