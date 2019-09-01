import ujson


class SensorManager:
    "SensorManager supervises different Sensors and produces logs."

    LOGFILE = "sensors.json"

    def __init__(self, sensors, logfile=LOGFILE):
        self._sensors = sensors
        self._logfile = logfile

    def dump_log(self):
        f = open(self._logfile, "a")
        for sensor in self._sensors:
            ujson.dump(sensor.to_dict(), f)
            f.write("\n")
        f.close()
