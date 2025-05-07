from plan_creator.constants import *
from plan_creator.plan_library.swim_builder import SwimBuilder
from plan_creator.plan_library.ride_builder import RideBuilder
from plan_creator.plan_library.run_builder import RunBuilder
import logging

class PlanDayBuilder:

    def __init__(self, paces, week_num, day_num, units):
        self.paces = paces
        self.week_num = week_num
        self.day_num = day_num
        self.units = units
        self.has_swim = False
        self.has_bike = False
        self.has_run = False
        self.has_strength = False
        self.discipline = []
        self.workout_type = []
        self.summary = []
        self.swim_builder = SwimBuilder(week_num, day_num)
        self.ride_builder = RideBuilder(week_num, day_num, units)
        self.run_builder = RunBuilder(week_num, day_num, units)

    def _get_distance(self, distance_km, distance_mi):
        if self.units == "km":
            return float(distance_km)
        elif self.units == "mi":
            return float(distance_mi)
        else:
            raise ValueError("Invalid units. Please use 'km' or 'mi'.")
        
    def _get_distance_rounded(self, distance_km, distance_mi):
        return int(round(self._get_distance(distance_km, distance_mi)))

    def _get_distance_km(self, distance_km):
        return float(distance_km)

    def add_swim(self, time, distance_km, distance_mi, hr_zone):
        self.has_swim = True
        distance = self._get_distance_km(distance_km)
        self.discipline.append("Swim")
        workout_type, summary = self.swim_builder.generate_swim_workout(time, distance, hr_zone)
        self.workout_type.append(workout_type)
        self.summary.append(summary)
        return self

    def add_bike(self, time, distance_km, distance_mi, hr_zone):
        self.has_bike = True
        distance = self._get_distance_rounded(distance_km, distance_mi)
        self.discipline.append("Bike")
        workout_type, summary = self.ride_builder.generate_ride_workout(time, distance, hr_zone)
        self.workout_type.append(workout_type)
        self.summary.append(summary)
        return self

    def add_run(self, time, distance_km, distance_mi, hr_zone):
        self.has_run = True
        distance = self._get_distance_rounded(distance_km, distance_mi)
        self.discipline.append("Run")
        workout_type, summary = self.run_builder.generate_run_workout(time, distance, hr_zone)
        self.workout_type.append(workout_type)
        self.summary.append(summary)
        return self

    def add_strength(self):
        self.has_strength = True
        self.discipline.append("Workout")
        self.workout_type.append("Stretch & Strength")
        self.summary.append("See the Stretch Routine & Strength Training section below")
        return self

    def build(self):
        # If no data is present, then its a rest day
        if not self.has_swim and not self.has_bike and not self.has_run and not self.has_strength:
            return {
                "Discipline": "Rest Day",
                "WorkoutType": "",
                "Summary": ""
            }

        # If only Bike and Run, then its a Brick workout
        if not self.has_swim and self.has_bike and self.has_run and not self.has_strength:
            cleaned_summary = []
            for i, item in enumerate(self.summary):
                cleaned_item = item.replace("Main Set:\n", "").strip()
                cleaned_summary.append(self.discipline[i] + " " + cleaned_item)
                if i % 2 == 0 and i + 1 < len(self.summary):
                    cleaned_summary.append("Immediate Transition")
            self.summary = cleaned_summary
            return {
                "Discipline": "Interdisciplinary",
                "WorkoutType": "Brick Workout",
                "Summary": "\n".join(self.summary)
            }

        processed_summary = self.summary.copy()
        if len(self.summary) > 1:
            processed_summary = [f"Workout {i + 1}:\n{item}" for i, item in enumerate(self.summary)]
        return {
            "Discipline": " & ".join(self.discipline),
            "WorkoutType": " & ".join(self.workout_type),
            "Summary": "\n\n".join(processed_summary)
        }

class PlanProcessor():

    # Create Logger
    logger = logging.getLogger(__name__)

    def __init__(self, paces, units):
        self.paces = paces
        self.units = units

    def process_plan(self, data):
        # Process the plan here
        training_plan_master = {}
        # Process the data: group every 5 rows as one week and every 5 columns as one day
        week_num = 0
        for week_start in range(0, len(data), 5):  # Iterate over weeks (5 rows at a time)
            week_num += 1
            self.logger.debug(f"Week Num: {week_num}")
            week_data = data[week_start:week_start + 5]  # Get 5 rows for the week
            week_output_data = {}
            day_num = 0
            for day_start in range(0, len(week_data[0]), 5):  # Iterate over days (5 columns at a time)
                day_num += 1
                self.logger.debug(f"Day Num: {day_num}")
                day_values = [week_row[day_start:day_start + 5] for week_row in week_data]  # Get 5 columns for the day
                self.logger.debug(f"Day Values: {day_values}")

                week_output_data[DAY_NUM_WEEK_MAP[day_num]] = self._parse_day_values(week_num, day_num, day_values)

            training_plan_master[f"Week {week_num}"] = week_output_data

        return training_plan_master

    def _parse_day_values(self, week_num, day_num, day_values):
        swim_data = day_values[0]
        bike_data = day_values[1]
        run_data = day_values[2]
        strength_data = day_values[3]

        plan_day_builder = PlanDayBuilder(self.paces, week_num, day_num, self.units)
        # Check if swim data is present
        if swim_data[0] != "":
            plan_day_builder.add_swim(swim_data[0], swim_data[1], swim_data[2], swim_data[3])
        # Check if bike data is present
        if bike_data[0] != "":
            plan_day_builder.add_bike(bike_data[0], bike_data[1], bike_data[2], bike_data[3])
        # Check if run data is present
        if run_data[0] != "":
            plan_day_builder.add_run(run_data[0], run_data[1], run_data[2], run_data[3])
        # Check if strength data is present
        if strength_data[0] != "":
            plan_day_builder.add_strength()
        
        return plan_day_builder.build()
