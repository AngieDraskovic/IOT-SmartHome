from collections import deque
import threading


class StateDus:
    def __init__(self):
        self._recent_distances = deque(maxlen=10)
        self._lock = threading.Lock()

    def add_distance(self, value):
        with self._lock:
            self._recent_distances.append(value)

    def get_recent_distances(self):
        with self._lock:
            return list(self._recent_distances)

    def analyze_movement(self):
        with self._lock:
            if len(self._recent_distances) < 4:
                return 0    # not enough data

            last_measurements = list(self._recent_distances)[-4:]   # racunam na osnovu ovoga

            average = sum(last_measurements) / len(last_measurements)   # trend na osnovu prosjeka
            current_distance = self._recent_distances[-1]

            if current_distance <= average:
                return 1
            elif current_distance > average:
                return -1
