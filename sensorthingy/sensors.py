import light_sensor


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


class LightSensor(Sensor):
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
