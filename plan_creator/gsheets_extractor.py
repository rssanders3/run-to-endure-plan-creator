import gspread
from oauth2client.service_account import ServiceAccountCredentials
from plan_creator.constants import *
import logging

# Create Logger
logger = logging.getLogger(__name__)

class GoogleSheetExtractor():

    def __init__(self, config_path:str, sheet_url: str, sheet_name: str, event_type: str):
        logger.info("Initializing GoogleSheetExtractor with config_path: %s, sheet_url: %s, sheet_name: %s, event_type: %s", config_path, sheet_url, sheet_name, event_type)
        self.config_path = config_path
        self.sheet_url = sheet_url
        self.sheet_name = sheet_name
        self.event_type = event_type

    def _get_or_create_worksheet(self):
        # Define the scope and authenticate
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.config_path, scope)
        client = gspread.authorize(creds)

        # Open your Google Sheet by name or by URL
        spreadsheet = client.open_by_url(self.sheet_url)
        worksheet = spreadsheet.worksheet(self.sheet_name)
        return worksheet

    def _get_cells_by_event_type(self):
        return SHEET_RANGE_MAP.get(self.event_type)

    def extract_paces(self):
        worksheet = self._get_or_create_worksheet()
        logger.info(f"Extracting paces from cells: {SWIM_PACE_CELL}, {BIKE_SPEED_CELL}, {RUN_PACE_CELL}")
        paces = {
            "swim_pace": worksheet.acell(SWIM_PACE_CELL).value,
            "bike_speed": worksheet.acell(BIKE_SPEED_CELL).value,
            "run_pace": worksheet.acell(RUN_PACE_CELL).value
        }
        logger.info(f"Extracted paces: {paces}")
        return paces

    def extract(self):
        """
        Extracts data from a Google Sheet and returns it as a list of dictionaries.
        """
        worksheet = self._get_or_create_worksheet()
        cells = self._get_cells_by_event_type()
        logger.info(f"Extracting data from cells: {cells}")
        return worksheet.get(cells)
