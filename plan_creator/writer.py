import csv
import logging

# Create Logger
logger = logging.getLogger(__name__)

class Writer:

    def __init__(self):
        pass

    def _convert_to_output_rows(self, training_plan_master):
        output_rows = []
        # Flatten and write training_plan_master to a CSV file
        for week, days in training_plan_master.items():
            output_rows.append(["Week", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
            week_disciplin_row = [week]
            week_workout_type_row = [week]
            week_summary_row = [week]
            for day, details in days.items():
                week_disciplin_row.append(details["Discipline"])
                week_workout_type_row.append(details["WorkoutType"])
                week_summary_row.append(details["Summary"])
            output_rows.append(week_disciplin_row)
            output_rows.append(week_workout_type_row)
            output_rows.append(week_summary_row)
            output_rows.append(["", "", "", "", "", "", "", ""])
        return output_rows

    def write(self, training_plan_master, output_path):
        raise NotImplementedError("Subclasses should implement this method.")

class CSVWriter(Writer):

    def write(self, training_plan_master, output_path):
        output_rows = self._convert_to_output_rows(training_plan_master)
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in output_rows:
                writer.writerow(row)
        logger.info(f"Data written to {output_path} successfully.")

class WriterBuilder:

    @staticmethod
    def get_writer(output_type):
        if output_type == "csv":
            return CSVWriter()
        else:
            raise ValueError(f"Unsupported output type: {output_type}")
