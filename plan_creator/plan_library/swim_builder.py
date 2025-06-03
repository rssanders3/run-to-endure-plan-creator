import textwrap
import logging

# Create Logger
logger = logging.getLogger(__name__)

class SwimBuilder:

    def __init__(self, week_num, day_num):
        self.week_num = week_num
        self.day_num = day_num
        self.units = "km"

    def generate_swim_workout(self, time, distance, hr_zone):
        """
        Generates a swim workout based on the distance and heart rate zone.

        Args:
            distance (float): The distance of the swim in kilometers or miles.
            hr_zone (int): The heart rate zone (1 to 5).

        Returns:
            tuple: A tuple containing two strings: workout type and workout summary.
        """
        distance_meters = distance * 1000
        main_distance = int(distance_meters - (200 + 200))  # 200m warmup and cooldown

        # todo: detect Open Water Swim
        if hr_zone == '1':
            workout_type = "Recovery Swim"
            main_set_distance = 50
            main_set_reps = int(main_distance / main_set_distance)
            summary = textwrap.dedent(f"""
            Warm Up:
            4x50m
            Main Set:
            {main_set_reps}x{main_set_distance}m (Focus on Technique)
            Cooldown:
            4x50m
            """).strip("\n")
        elif hr_zone == '2':
            workout_type = "Easy Swim"
            main_set_distance = 100
            main_set_reps = int(main_distance / main_set_distance)
            summary = textwrap.dedent(f"""
            TODO: REVIEW THIS:
            Warm Up:
            4x50m
            Main Set:
            {main_set_reps}x{main_set_distance}m (Focus on Technique)
            Cooldown:
            4x50m
            """).strip("\n")
        elif hr_zone == '3':
            workout_type = "Tempo Swim"
            main_set_distance = 100
            main_set_reps = int(main_distance / main_set_distance)
            summary = textwrap.dedent(f"""
            TODO: REVIEW THIS:
            Warm Up:
            4x50m
            Main Set:
            {main_distance}-{self.units} @ Z3 (RPE: 6)
            Cooldown:
            4x50m                       
            """).strip("\n")
        elif hr_zone == '4':
            workout_type = "Threshold Swim"
            summary = textwrap.dedent(f"""
            TODO: REVIEW THIS:
            Distance: {distance}-{self.units}
            HR Zone: {hr_zone}                   
            """).strip("\n")
        elif hr_zone == '5':
            workout_type = "Interval Swim"
            summary = textwrap.dedent(f"""
            TODO: REVIEW THIS:
            Distance: {distance}-{self.units}
            HR Zone: {hr_zone}
            """).strip("\n")
        else:
            raise ValueError(f"Heart Rate Zone '{hr_zone}' is invalid. Please use a value between 1 and 5. (Other Row Details: Week: {self.week_num}, Day: {self.day_num}, Time: {time}, Distance: {distance}, HR Zone: {hr_zone})")

        return workout_type, summary