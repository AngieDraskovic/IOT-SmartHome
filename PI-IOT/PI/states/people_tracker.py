class PeopleTracker:

    def __init__(self, room):
        self._room = room
        self._people_count = 0

    def entry(self):
        self._people_count += 1

    def exit(self):
        if self._people_count > 0:
            self._people_count -= 1

    def get_people_count(self):
        return self._people_count

    def __str__(self):
        return f"Room: {self._room}, People Count: {self._people_count}"
