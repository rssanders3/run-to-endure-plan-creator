from plan_creator.gsheets_extractor import GoogleSheetExtractor
from plan_creator.plan_processor import PlanProcessor
from plan_creator.writer import *
from plan_creator.constants import *
import os
import logging

# Create Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Import necessary environment variables
    logger.info("Importing environment variables")
    GOOGLE_CONFIG_PATH = os.environ["GOOGLE_CONFIG_PATH"]
    SPREADSHEET_URL = os.environ["SPREADSHEET_URL"]
    SHEET_NAME = os.environ["SHEET_NAME"]
    EVENT_TYPE = os.environ["EVENT_TYPE"]
    OUTPUT_TYPE = os.environ["OUTPUT_TYPE"]
    OUTPUT_PATH = os.environ["OUTPUT_PATH"]
    UNITS = os.environ["UNITS"]
    logger.info(
        "Environment variables imported successfully:\n"
        "GOOGLE_CONFIG_PATH: %s\n"
        "SPREADSHEET_URL: %s\n"
        "SHEET_NAME: %s\n"
        "EVENT_TYPE: %s\n"
        "OUTPUT_TYPE: %s\n"
        "OUTPUT_PATH: %s\n"
        "UNITS: %s\n",
        GOOGLE_CONFIG_PATH,
        SPREADSHEET_URL,
        SHEET_NAME,
        EVENT_TYPE,
        OUTPUT_TYPE,
        OUTPUT_PATH,
        UNITS
    )

    # Create Google Sheets Extractor instance
    logger.info("Creating GoogleSheetExtractor instance")
    extractor = GoogleSheetExtractor(GOOGLE_CONFIG_PATH, SPREADSHEET_URL, SHEET_NAME, EVENT_TYPE)
    logger.info("GoogleSheetExtractor instance created successfully")
    # Extract paces from Google Sheets
    logger.info("Extracting paces from Google Sheets")
    paces = extractor.extract_paces()
    logger.info("Paces extracted successfully: %s", paces)
    # Extract data from Google Sheets
    logger.info("Extracting data from Google Sheets")
    data = extractor.extract()

    # Parse Plan
    logger.info("Parsing plan")
    plan_processor = PlanProcessor(paces, UNITS)
    training_plan_master = plan_processor.process_plan(data)
    logger.info("Plan parsed successfully")

    # Write to Output
    logger.info("Writing data to output")
    writer = WriterBuilder.get_writer(OUTPUT_TYPE)
    writer.write(training_plan_master, OUTPUT_PATH)

if __name__=="__main__":
    main()
