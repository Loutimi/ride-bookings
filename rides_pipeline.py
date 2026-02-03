import logging
import pandas as pd
from ride_params import ncr_ride_bookings


class RideBookings:
    """
    Pipeline for loading, cleaning, validating, and preparing NCR ride booking data.
    
    This class handles:
    - Logging configuration
    - Reading the CSV file
    - Detecting duplicate rows
    - Cleaning specific string-based columns
    - Running a full data preparation pipeline
    """

    def __init__(self, csv_path=ncr_ride_bookings, logging_level="INFO"):
        """
        Initialize the RideBookings pipeline.

        Parameters
        ----------
        csv_path : str, optional
            Path to the source CSV file.
        logging_level : str, optional
            Logging verbosity level (DEBUG, INFO, WARNING, ERROR).
        """
        self.initialize_logging(logging_level)
        self.df = None
        self.csv_path = csv_path

    def initialize_logging(self, logging_level):
        """
        Set up logging for the RideBookings pipeline.

        Parameters
        ----------
        logging_level : str
            Logging verbosity level.
        """
        logger_name = __name__ + ".RideBookings"
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = False

        log_level = getattr(logging, logging_level.upper(), logging.INFO)
        self.logger.setLevel(log_level)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def read_csv_file(self):
        """
        Load the CSV file into a pandas DataFrame.

        Returns
        -------
        DataFrame
            The loaded dataset.

        Raises
        ------
        EmptyDataError
            If the file is empty or incorrect.
        Exception
            Any other file reading issue.
        """
        try:
            self.df = pd.read_csv(self.csv_path)
            self.logger.info("CSV file read successfully.")
            return self.df

        except pd.errors.EmptyDataError as exc:
            self.logger.error(
                "The file path does not point to a valid CSV. "
                "Check ride_params.py and try again."
            )
            raise exc

        except Exception as exc:
            self.logger.error(f"Failed to read CSV. Error: {exc}")
            raise exc

    def number_of_duplicates(self, subset=None):
        """
        Count duplicate rows in the dataset.

        Parameters
        ----------
        subset : list of str, optional
            Columns to check for duplicates. If None, checks entire rows.

        Returns
        -------
        int
            Number of duplicate rows detected.

        Raises
        ------
        ValueError
            If the CSV has not been loaded.
        """
        if self.df is None:
            raise ValueError("CSV not loaded. Call read_csv_file() first.")

        dup_count = self.df.duplicated(subset=subset).sum()

        if dup_count > 0:
            if subset:
                self.logger.info(
                    f"Dataset contains {dup_count} duplicates based on {subset}."
                )
            else:
                self.df = self.df.drop_duplicates()
                self.logger.info(
                    f"{dup_count} exact duplicate rows in the Dataset have been dropped"
                )
        else:
            if subset:
                self.logger.info(f"No duplicates found based on {subset}.")
            else:
                self.logger.info("No exact duplicate rows found.")

        return dup_count

    def clean_columns(self, value):
        """
        Clean individual cell values: strips whitespace and removes quotes.

        Parameters
        ----------
        value : any
            Cell value to clean.

        Returns
        -------
        any
            Cleaned value if string; otherwise unchanged.
        """
        if isinstance(value, str):
            return value.strip().replace('"', "")
        return value

    def check_blanks_in_columns(self):
        """
        Log the number of blank (NaN) values in each column of the DataFrame.

        Uses the logger to report counts for all columns.
        """
        if self.df is None:
            self.logger.warning("DataFrame not loaded. Call read_csv_file() first.")
            return

        for column in self.df.columns:
            empty_rows = self.df[column].isna().sum() + (self.df[column] == '').sum()
            self.logger.info(f"{column} column contains {empty_rows} blank values.")


    def apply_corrections(self):
        """
        Apply cleaning rules to specific columns in the DataFrame.

        Cleans:
        - 'Customer ID'
        - 'Booking ID'
        """
        if self.df is not None:
            cols_to_clean = ["Customer ID", "Booking ID"]
            for col in cols_to_clean:
                self.df[col] = self.df[col].apply(self.clean_columns)

    def load_pipeline(self):
        """
        Execute the complete data loading and cleaning pipeline.

        Steps:
        1. Read CSV file
        2. Check for duplicates
        3. Clean selected columns
        4. Log the number of blank (NaN) values in each column of the DataFrame.
        """
        self.read_csv_file()
        self.number_of_duplicates()
        self.apply_corrections()
        self.check_blanks_in_columns()
