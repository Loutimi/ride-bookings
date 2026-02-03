import pandas as pd
import pytest
from unittest.mock import patch
from rides_pipeline import RideBookings


@pytest.fixture
def pipeline():
    """Create a RideBookings instance without reading the actual CSV."""
    rb = RideBookings(csv_path="dummy_path.csv")
    return rb


@pytest.fixture
def sample_df():
    """A small mock DataFrame that mimics the structure of the real data."""
    return pd.DataFrame({
        "Customer ID": [' "C001" ', "C002", "C003", "C003"],
        "Booking ID": [' "B101" ', "B102", "B103", "B103"],
        "Pickup Location": ["Delhi", "Mumbai", "Delhi", "Delhi"],
        "Dropoff Location": ["Noida", "Pune", "Noida", "Noida"],
        "Fare": [150.0, 200.0, 150.0, 150.0],
    })


class TestReadCSV:
    def test_read_csv_loads_dataframe(self, pipeline):
        """Pipeline should load a valid CSV into self.df."""
        mock_df = pd.DataFrame({"Customer ID": ["C001"], "Booking ID": ["B101"]})
        with patch("pandas.read_csv", return_value=mock_df):
            result = pipeline.read_csv_file()
        assert result is not None
        assert isinstance(pipeline.df, pd.DataFrame)
        assert len(pipeline.df) == 1

    def test_read_csv_raises_on_empty_file(self, pipeline):
        """Pipeline should raise EmptyDataError for an empty or invalid file."""
        with patch("pandas.read_csv", side_effect=pd.errors.EmptyDataError):
            with pytest.raises(pd.errors.EmptyDataError):
                pipeline.read_csv_file()

    def test_read_csv_raises_on_generic_error(self, pipeline):
        """Pipeline should raise on any other file-reading failure."""
        with patch("pandas.read_csv", side_effect=FileNotFoundError("No file")):
            with pytest.raises(FileNotFoundError):
                pipeline.read_csv_file()


class TestDuplicates:
    def test_raises_if_csv_not_loaded(self, pipeline):
        """Should raise ValueError if read_csv_file() hasn't been called."""
        with pytest.raises(ValueError, match="CSV not loaded"):
            pipeline.number_of_duplicates()

    def test_detects_exact_duplicates(self, pipeline, sample_df):
        """Should correctly count exact duplicate rows."""
        pipeline.df = sample_df.copy()
        count = pipeline.number_of_duplicates()
        # Rows at index 2 and 3 are identical -> 1 duplicate
        assert count == 1

    def test_drops_exact_duplicates(self, pipeline, sample_df):
        """After calling number_of_duplicates(), exact duplicates should be removed."""
        pipeline.df = sample_df.copy()
        pipeline.number_of_duplicates()
        # 4 rows originally, 1 duplicate dropped -> 3 unique rows
        assert len(pipeline.df) == 3

    def test_detects_subset_duplicates(self, pipeline, sample_df):
        """Should count duplicates based on a column subset without dropping rows."""
        pipeline.df = sample_df.copy()
        count = pipeline.number_of_duplicates(subset=["Customer ID"])
        # "C003" appears twice -> 1 duplicate on that subset
        assert count == 1
        # Subset mode should NOT drop rows
        assert len(pipeline.df) == 4

    def test_no_duplicates(self, pipeline):
        """Should return 0 when there are no duplicates."""
        pipeline.df = pd.DataFrame({
            "Customer ID": ["C001", "C002"],
            "Booking ID": ["B101", "B102"],
        })
        assert pipeline.number_of_duplicates() == 0


class TestCleanColumns:
    def test_strips_whitespace_and_quotes(self, pipeline):
        """Should remove leading/trailing whitespace and embedded quotes."""
        assert pipeline.clean_columns(' "C001" ') == "C001"

    def test_leaves_non_string_unchanged(self, pipeline):
        """Numeric or None values should pass through untouched."""
        assert pipeline.clean_columns(42) == 42
        assert pipeline.clean_columns(None) is None
        assert pipeline.clean_columns(3.14) == 3.14


class TestApplyCorrections:
    def test_cleans_target_columns(self, pipeline, sample_df):
        """Customer ID and Booking ID should be stripped and unquoted."""
        pipeline.df = sample_df.copy()
        pipeline.apply_corrections()
        assert pipeline.df["Customer ID"].iloc[0] == "C001"
        assert pipeline.df["Booking ID"].iloc[0] == "B101"

    def test_does_not_touch_other_columns(self, pipeline, sample_df):
        """Columns not in cols_to_clean should remain unchanged."""
        pipeline.df = sample_df.copy()
        original_pickup = pipeline.df["Pickup Location"].tolist()
        pipeline.apply_corrections()
        assert pipeline.df["Pickup Location"].tolist() == original_pickup

    def test_does_nothing_if_df_is_none(self, pipeline):
        """Should not raise an error if df hasn't been loaded yet."""
        pipeline.df = None
        pipeline.apply_corrections()  # Should simply do nothing


class TestCheckBlanks:
    def test_logs_blank_counts(self, pipeline, caplog):
        """Should log the correct number of blanks per column."""
        pipeline.df = pd.DataFrame({
            "Customer ID": ["C001", None, "C003"],
            "Booking ID": ["B101", "B102", ""],
        })
        pipeline.logger.propagate = True
        with caplog.at_level("INFO", logger="rides_pipeline.RideBookings"):
            pipeline.check_blanks_in_columns()

        assert "Customer ID column contains 1 blank values" in caplog.text
        assert "Booking ID column contains 1 blank values" in caplog.text

    def test_warns_if_df_not_loaded(self, pipeline, caplog):
        """Should log a warning and return early if df is None."""
        pipeline.df = None
        pipeline.logger.propagate = True
        with caplog.at_level("WARNING", logger="rides_pipeline.RideBookings"):
            pipeline.check_blanks_in_columns()
        assert "DataFrame not loaded" in caplog.text


class TestLoadPipeline:
    def test_full_pipeline_runs_without_error(self, pipeline, sample_df):
        """The full pipeline should execute end-to-end cleanly."""
        with patch.object(pipeline, "read_csv_file", side_effect=lambda: setattr(pipeline, "df", sample_df.copy())):
            pipeline.load_pipeline()

        # Duplicates dropped: 4 -> 3
        assert len(pipeline.df) == 3
        # Cleaning applied
        assert pipeline.df["Customer ID"].iloc[0] == "C001"
        assert pipeline.df["Booking ID"].iloc[0] == "B101"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
