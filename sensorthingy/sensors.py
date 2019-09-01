import bme680
import light_sensor
import power


class Sensor:
    "Sensor is an abstract class for a generic sensor."

    def __init__(self, name):
        self.name = name

    @property
    def fields(self):
        "fields should return a list of names of the returned values."
        pass

    def read_values(self, **kwargs):
        """ read_values reads the latest values from the Sensor and returns
            them as a list, in the same order as returned by fields.
        """
        pass


class EnvironmentalSensor(Sensor):
    "EnvironmentalSensor reads environmental values from the BME680 sensor."

    def __init__(self):
        super().__init__("Environmental Sensor")

    @property
    def fields(self):
        return ["Temperature (C)", "Humidity (% r.h.)",
                "Pressure (hPa)", "Gas resistance (Ohm)"]

    def read_values(self, **kwargs):
        bme680.init()
        data = bme680.get_data()
        bme680.deinit()

        return list(data)


class LightSensor(Sensor):
    "LightSensor reads the values from the onboard IR-LED."

    def __init__(self):
        super().__init__("Light Sensor")

    @property
    def fields(self):
        return ["Brightness Value", "Brightness Description"]

    def read_values(self, **kwargs):
        light_sensor.start()
        bright = light_sensor.get_reading()
        light_sensor.stop()

        if bright < 7:
            bright_desc = "Very very dark"
        elif bright < 15:
            bright_desc = "Very dark"
        elif bright < 50:
            bright_desc = "Hackerspace brightness"
        elif bright < 100:
            bright_desc = "Not so dark"
        else:
            bright_desc = "Sunlight"

        return [bright, bright_desc]


class PowerSensor(Sensor):
    "PowerSensor reads the card10's power status."

    def __init__(self):
        super().__init__("Power Sensor")

    @property
    def fields(self):
        return ["Battery Voltage (V)", "Battery Current (A)",
                "Charge Voltage (V)", "Charge Current (A)"]

    def read_values(self, **kwargs):
        return [power.read_battery_voltage(), power.read_battery_current(),
                power.read_chargein_voltage(), power.read_chargein_current()]
