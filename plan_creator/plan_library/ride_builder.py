import textwrap
import logging

# Create Logger
logger = logging.getLogger(__name__)

class RideBuilder:

    def __init__(self, week_num, day_num, units):
        self.week_num = week_num
        self.day_num = day_num
        self.units = units

    def generate_ride_workout(self, time, distance, hr_zone):
        """
        Generates a ride workout based on the distance and heart rate zone.

        Args:
            distance (float): The distance of the ride in kilometers or miles.
            hr_zone (int): The heart rate zone (1 to 5).

        Returns:
            tuple: A tuple containing two strings: workout type and workout summary.
        """
        if hr_zone == '1':
            workout_type = "Recovery Ride"
            summary = textwrap.dedent(f"""
            Main Set:
            {distance}-{self.units} @ Z1 (RPE: 3)
            """).lstrip("\n")
        elif hr_zone == '2':
            # Handle as Long Ride as well
            workout_type = "Easy Ride"
            summary = textwrap.dedent(f"""
            Main Set:
            {distance}-{self.units} @ Z2 (RPE: 5)
            """).lstrip("\n")
        elif hr_zone == '3':
            # Set as Tempo Ride
            workout_type = "Interval Ride"
            summary = textwrap.dedent(f"""
            Warm Up:
            3-km @ Z1 (RPE: 3)
            Main Set:
            3x 30-seconds at Z4 (RPE: 8) then 8-minutes @ Z3 (RPE: 7)
            Warm Up:
            3-km @ Z1 (RPE: 3)
            Main Set:
            {distance}-{self.units} @ Z3 (RPE: 6)
            """).lstrip("\n")
        elif hr_zone == '4':
            workout_type = "Interval Ride"
            summary = textwrap.dedent(f"""
            Main Set:
            {distance}-{self.units} @ Z4 (RPE: 7)
            """).lstrip("\n")
        elif hr_zone == '5':
            workout_type = "Interval Ride"
            summary = textwrap.dedent(f"""
            TODO - FIGURE OUT
            Distance: {distance}-{self.units}
            HR Zone: {hr_zone}
            """).lstrip("\n")
        else:
            raise ValueError(f"Heart Rate Zone '{hr_zone}' is invalid. Please use a value between 1 and 5. (Other Row Details: Week: {self.week_num}, Day: {self.day_num}, Time: {time}, Distance: {distance}, HR Zone: {hr_zone})")

        return workout_type, summary
