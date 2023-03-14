import sys
import clr
import logging.handlers
from Database import DB


def handle_exception(exc_type, exc_value, exc_traceback):
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


def initialize_openhardwaremonitor():
    file = 'OpenHardwareMonitorLib'
    clr.AddReference(file)

    from OpenHardwareMonitor import Hardware

    handle = Hardware.Computer()
    handle.MainboardEnabled = True
    handle.CPUEnabled = True
    handle.RAMEnabled = True
    handle.GPUEnabled = True
    handle.HDDEnabled = True
    handle.Open()
    return handle.Hardware


def monitor_vitals():
    sensors = ["GPU Core", "CPU Package", "CPU Total"]
    data = dict((i, {"Temperature": None, "Load": None}) for i in sensors)
    for i in hardware:
        if i.get_HardwareType() in (2, 4, 5):
            i.Update()
            for j in i.get_Sensors():
                if j.get_Name() in sensors:
                    if j.get_SensorType() == 2:
                        data[j.get_Name()]["Temperature"] = j.get_Value()
                    elif j.get_SensorType() == 3:
                        data[j.get_Name()]["Load"] = j.get_Value()

    values = (data["CPU Package"]["Temperature"], data["CPU Total"]["Load"], data["GPU Core"]["Temperature"],
              data["GPU Core"]["Load"])
    db.write_sensor_data(values)
    logger.info("Wrote to database: %s", values)


if __name__ == '__main__':
    sys.excepthook = handle_exception

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    fh = logging.handlers.TimedRotatingFileHandler("logs/vitalmon.log", when="D", interval=30)
    fh.setLevel(logging.INFO)
    form = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
    fh.setFormatter(form)
    logger.addHandler(fh)

    hardware = initialize_openhardwaremonitor()
    db = DB()
    monitor_vitals()
