import textwrap
import logging

# Create Logger
logger = logging.getLogger(__name__)

class RunBuilder:

    def __init__(self, week_num, day_num, units):
        self.week_num = week_num
        self.day_num = day_num
        self.units = units

    def get_warmup_and_cooldown_distance(self):
        if self.units == "km":
            return 1.0
        elif self.units == "mi":
            return 0.5
        else:
            raise ValueError("Invalid units. Please use 'km' or 'mi'.")

    def generate_run_workout(self, time, distance, hr_zone):
        """
        Generates a run workout based on the distance and heart rate zone.

        Args:
            distance (float): The distance of the run in kilometers or miles.
            hr_zone (int): The heart rate zone (1 to 5).

        Returns:
            tuple: A tuple containing two strings: workout type and workout summary.
        """
        if hr_zone == '1':
            workout_type = "Recovery Run"
            summary = textwrap.dedent(f"""
            Main Set:
            {distance}-{self.units} @ Z1 (RPE: 3)
            """).lstrip("\n")
        elif hr_zone == '2':
            # Handle as Long Run as well
            workout_type = "Easy Run"
            summary = textwrap.dedent(f"""
            Main Set:
            {distance}-{self.units} @ Z2 (RPE: 5)
            """).lstrip("\n")
        elif hr_zone == '3':
            workout_type = "Tempo Run"
            warmup_distance = self.get_warmup_and_cooldown_distance()
            cooldown_distance = self.get_warmup_and_cooldown_distance()
            main_distance = distance - (warmup_distance + cooldown_distance)
            # todo: set pace
            summary = textwrap.dedent(f"""
            Warm Up:
            {warmup_distance}-{self.units} @ Z1 (RPE: 3)
            Running Form Drills (Butt Kicks, High Knees, etc.)
            Main Set:
            {main_distance}-{self.units} @ Z3 (RPE: 7)
            Cool Down:
            {cooldown_distance}-{self.units} @ Z1 (RPE: 3)
            """).lstrip("\n")
        elif hr_zone == '4':
            workout_type = "Interval Run"
            warmup_distance = self.get_warmup_and_cooldown_distance()
            cooldown_distance = self.get_warmup_and_cooldown_distance()
            # todo: set pace and number of intervals
            summary = textwrap.dedent(f"""
            Main Set:
            Warm Up:
            {warmup_distance}-{self.units} @ Z1 (RPE: 3)
            Running Form Drills (Butt Kicks, High Knees, etc.)
            Main Set:
            5x1-km @ 5:15/km Pace with 1-min rest - TODO - FIGURE OUT
            Cool Down:
            {cooldown_distance}-{self.units} @ Z1 (RPE: 3)
            """).lstrip("\n")
        elif hr_zone == '5':
            workout_type = "Interval Run"
            summary = textwrap.dedent(f"""
            TODO - FIGURE OUT
            Distance: {distance}-{self.units}
            HR Zone: {hr_zone}
            """).lstrip("\n")
        else:
            raise ValueError(f"Heart Rate Zone '{hr_zone}' is invalid. Please use a value between 1 and 5. (Other Row Details: Week: {self.week_num}, Day: {self.day_num}, Time: {time}, Distance: {distance}, HR Zone: {hr_zone})")

        return workout_type, summary
