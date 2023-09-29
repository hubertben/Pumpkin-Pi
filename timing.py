
import time
import matplotlib.pyplot as plt


def currentTime():
    return round(time.time(), 2)

class Timer:

    def __init__(self, timer_id, start_time = None):
        self.timer_id       = timer_id
        self.start_time     = start_time if(start_time) else currentTime()
        self.stop_time      = -1
        self.elapsed_time   = -1

        self.markers = []
        self.isRunning = start_time is None


    def start(self, start_time = None):
        self.start_time = start_time if(start_time) else currentTime()
        self.isRunning = True


    def stop(self, stop_time = None):
        self.stop_time = stop_time if(stop_time) else currentTime()
        self.isRunning = False
        self.computeElapsed()


    def computeElapsed(self):
        self.elapsed_time = self.stop_time - self.start_time


    def getStartTime(self):
        return self.start_time


    def getStopTime(self):
        return self.stop_time


    def getElapsedTime(self):
        self.computeElapsed()
        return self.elapsed_time


    def mark(self, notes = ""):
        self.markers.append({"time_stamp": currentTime(), "notes": notes})


    def __repr__(self):
        return f"{self.timer_id}: Start: {self.getStartTime()}, Stop: {self.getStopTime}, Elapsed: {self.getElapsedTime()}"
    

    def __str__(self):
        return f"{self.timer_id}: Start: {self.getStartTime()}, Stop: {self.getStopTime}, Elapsed: {self.getElapsedTime()}"


class TimeManager:
    def __init__(self):
        self.timers = {}
        self.creation_time = currentTime()


    def contains(self, timer_id):
        return (timer_id in self.timers)


    def addTimer(self, timer_id):
        if(self.contains(timer_id)):
            timer_id += "_"

        self.timers[timer_id] = Timer(timer_id)


    def startTimer(self, timer_id, start_time = None):
        if(self.contains(timer_id)):
            self.getTimer(timer_id).start(start_time)


    def stopTimer(self, timer_id, stop_time = None):
        T = self.getTimer(timer_id)
        if(T and T.isRunning):
            T.stop(stop_time)


    def markTimer(self, timer_id, notes = ""):
        if(self.contains(timer_id)):
            self.getTimer(timer_id).mark(notes)


    def getTimer(self, timer_id):
        if(self.contains(timer_id)):
            return self.timers[timer_id]
        

    def returnEvents(self, reduced=True):
        events = []
        scale = self.creation_time
        if not reduced:
            scale = 0

        for timer_id, timer in self.timers.items():
            events.append({
                'event_str': f"[START]     {timer_id} at time: {round(timer.getStartTime() - scale, 2)}",
                'time': round(timer.getStartTime() - scale, 2)
            })
            
            if timer.getStopTime() != -1:
                events.append({
                    'event_str': f"[STOP]      {timer_id} at time: {round(timer.getStopTime() - scale, 2)}",
                    'time': round(timer.getStopTime() - scale, 2)
                })
            
            for marker in timer.markers:
                events.append({
                    'event_str': f"[MARKER]    {timer_id} at time: {round(marker['time_stamp'] - scale, 2)} Notes: {marker['notes']}",
                    'time': round(marker['time_stamp'] - scale, 2)
                })
        
        events.sort(key=lambda x: x['time'])

        prev_time = 0
        formatted_events = []
        for event in events:
            time_diff = event['time'] - prev_time
            if(time_diff > 0.01):
                formatted_events.append(f"{event['event_str']} (+{time_diff:.2f}s)")
            else:
                formatted_events.append(f"{event['event_str']}")
            
            prev_time = event['time']

        return formatted_events


    def startAll(self):
        C = currentTime()
        for timer_id in self.timers.keys():
            self.startTimer(timer_id, C)


    def stopAll(self):
        C = currentTime()
        for timer_id in self.timers.keys():
            self.stopTimer(timer_id, C)


    def markAll(self, notes = ""):
        for timer_id in self.timers.keys():
            self.markTimer(timer_id, notes)


    def map(self, x, a, b, c, d):
        return c + (x - a) * (d - c) / (b - a)


    def adjust_x_values(self, time_stamps, threshold=0.1):
        adjusted_x = [0]

        difference = []
        for i in range(1, len(time_stamps)):
            difference.append(time_stamps[i] - time_stamps[i-1])

        max_dist = max(difference)
        for i in range(1, len(time_stamps)):
            difference = time_stamps[i] - time_stamps[i-1]
            adjusted_x.append(adjusted_x[-1] + (0.35 if difference < threshold else self.map((1 + difference), 1, max_dist, 1, 2)))

        return adjusted_x


    def plotStatistics(self):
        events = self.returnEvents(reduced=True)

        timer_ids = [f"{i}-{' '.join(event.split()[0 : event.split().index('at')]).rstrip('_')}" for i, event in enumerate(events)]
        time_stamps = [float(event.split("at time: ")[1].split()[0]) for event in events]

        sum_time = [time_stamps[0]]
        for i in range(1, len(time_stamps)):
            sum_time.append(sum_time[-1] + (time_stamps[i] - time_stamps[i-1]))

        adjusted_x_values = self.adjust_x_values(time_stamps)

        plt.figure(figsize=(12, 8))
        plt.plot(adjusted_x_values, sum_time, marker='o', color='purple', linestyle='-')

        plt.title('Cumulative Time for Each Event')
        plt.xlabel('Event (EventNumber-TimerID)')
        plt.ylabel('Cumulative Time (seconds)')
        plt.xticks(adjusted_x_values, timer_ids, rotation=90)
        plt.grid(True)

        plt.tight_layout()
        plt.show()


    def time_(self, timer_id):
        def decorator(fn):
            def wrapper(*args, **kwargs):
                self.addTimer(timer_id)
                result = fn(*args, **kwargs)
                self.stopTimer(timer_id)
                return result
            return wrapper
        return decorator