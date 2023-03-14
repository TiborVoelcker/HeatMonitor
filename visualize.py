from Database import DB
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter


class Visualizer:
    def __init__(self):
        self.db = DB()

    def get_data(self, sensor):
        query = '''
        SELECT
            time, temperature, load
        FROM
            "XMG-A507".temperature
        WHERE
            sensor=%s;
        '''
        res = np.array(self.db.execute_query(query, (sensor,)))
        return res.transpose()

    def plot(self):
        sensors = ["GPU Core", "CPU Core #1", "CPU Core #2", "CPU Core #3", "CPU Core #4"]
        fig = plt.figure()
        for i, sensor in enumerate(sensors):
            time, temp, load = self.get_data(sensor)
            load_filt = savgol_filter(load, 3, 1)
            fig = plt.figure()
            ax1 = fig.add_subplot(5, 1, i+1)
            try:
                health = temp/load_filt
            except ZeroDivisionError:
                health = temp
            ax1.plot(health)
            ax1.plot(savgol_filter(health, 31, 1))
            # fig.autofmt_xdate()
        plt.show()


vis = Visualizer()
vis.plot()
