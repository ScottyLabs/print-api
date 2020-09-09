from datetime import datetime
import pytz


class Printer:
    def __init__(self, name, signal, lcd_message, status, tray_status, as_of):
        self.name = name
        self.signal = signal
        self.lcd_message = lcd_message
        self.status = status
        self.tray_statuses = tray_status.split()
        self.as_of = as_of

        self.color = "Color" in name

    def time_diff(self):
        us_east = pytz.timezone("US/Eastern")
        now = datetime.now().astimezone()
        parsed = datetime.strptime(self.as_of, "%I:%M:%S %p")
        parsed = us_east.localize(
            parsed.replace(
                year=now.year,
                month=now.month,
                day=now.day,
                microsecond=now.microsecond,
            )
        )
        diff = now - parsed
        if diff.days < 0:
            parsed = parsed.replace(day=(now.day - 1))
            diff = now - parsed
        return diff
