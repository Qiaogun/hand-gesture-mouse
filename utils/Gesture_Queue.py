from collections import Counter


class Gesture_queue():
    def __init__(self, maxsize=5):
        self.gesture_queue = []
        self.maxsize = maxsize

    def enqueue(self, data):
        if len(self.gesture_queue) < (self.maxsize):
            self.gesture_queue.append(data)
        elif len(self.gesture_queue) == (self.maxsize):
            self.gesture_queue.pop(0)
            self.gesture_queue.append(data)

    def get_max_queue(self):
        if len(self.gesture_queue) == 0:
            return "None"
        if Counter(self.gesture_queue).most_common()[0][1] > 3:
            return Counter(self.gesture_queue).most_common()[0][0]


class Time_counters(object):
    def __init__(self):
        self.step_counter = 0
        self.flag = 0

    def update(self):
        if self.flag == 1:
            if self.step_counter > 45:
                self.step_counter = 0
                self.flag = 0
                #print("reset")
            self.step_counter += 1
