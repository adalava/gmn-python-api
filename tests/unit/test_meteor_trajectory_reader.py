"""Tests for the meteor_trajectory_reader module."""
import os
import unittest
from pathlib import Path

from tests.unit.expected_meteor_trajectory_reader_values import EXPECTED_COLUMN_NAMES
from tests.unit.expected_meteor_trajectory_reader_values import EXPECTED_COLUMN_NAMES_CAMEL_CASE
from tests.unit.expected_meteor_trajectory_reader_values import EXPECTED_DTYPES

from gmn_python_api import meteor_trajectory_reader as msr
from gmn_python_api.meteor_trajectory_schema import \
    get_model_meteor_trajectory_dataframe


class TestMeteorTrajectoryReader(unittest.TestCase):
    """Tests for the meteor_trajectory_reader module."""

    def setUp(self) -> None:
        """
        Sets up the tests.
        """
        self.mock_data_directory_csv = Path(
            os.path.join(
                os.path.dirname(__file__),
                "test_data",
                "traj_summary_monthly_201812.txt",
            )
        )

        self.mock_rest_api_csv = Path(
            os.path.join(
                os.path.dirname(__file__),
                "test_data",
                "rest_api_meteor_summary.txt"
            )
        )

    def test_read_csv_model_meteor_trajectory_file(self) -> None:
        """
        Test: That read_csv produces the expected dataframe with the model meteor
         trajectory file.
        When: read_csv is called with the model meteor trajectory file.
        """
        actual_dataframe = get_model_meteor_trajectory_dataframe()

        self.assertFalse(actual_dataframe.empty)
        self.assertEqual((534, 85), actual_dataframe.shape)
        self.assertEqual(
            ["20220304220741_yrPTs", "20220304221458_vpeSU", "20220304221734_ii908"],
            actual_dataframe.index.tolist()[:3],
        )
        self.assertEqual(EXPECTED_DTYPES, actual_dataframe.dtypes.tolist())
        self.assertEqual(EXPECTED_COLUMN_NAMES, actual_dataframe.columns.tolist())
        self.assertEqual("Unique trajectory (identifier)", actual_dataframe.index.name)

    def test_read_csv_model_meteor_trajectory_file_camel_case(self) -> None:
        """
        Test: That read_csv produces the expected dataframe with the model meteor
         trajectory file.
        When: read_csv is called with the model meteor trajectory file and
         output_camel_case is True.
        """
        actual_dataframe = get_model_meteor_trajectory_dataframe(output_camel_case=True)

        self.assertFalse(actual_dataframe.empty)
        self.assertEqual((534, 85), actual_dataframe.shape)
        self.assertEqual(
            ["20220304220741_yrPTs", "20220304221458_vpeSU", "20220304221734_ii908"],
            actual_dataframe.index.tolist()[:3],
        )
        self.assertEqual(EXPECTED_DTYPES, actual_dataframe.dtypes.tolist())
        self.assertEqual(EXPECTED_COLUMN_NAMES_CAMEL_CASE, actual_dataframe.columns.tolist())
        self.assertEqual("unique_trajectory_identifier", actual_dataframe.index.name)

    def test_read_csv_with_data_directory_data(self) -> None:
        """
        Test: That read_csv produces the expected dataframe with mock data directory
         data.
        When: read_csv is called with mock data directory data.
        """
        actual_dataframe = msr.read_csv(self.mock_data_directory_csv.read_text())

        self.assertFalse(actual_dataframe.empty)
        self.assertEqual((497, 85), actual_dataframe.shape)
        self.assertEqual(
            ["20181210010656_eBlUM", "20181210012238_ucxkx", "20181210024213_c2bJq"],
            actual_dataframe.index.tolist()[:3],
        )
        self.assertEqual(EXPECTED_DTYPES, actual_dataframe.dtypes.tolist())
        self.assertEqual(EXPECTED_COLUMN_NAMES, actual_dataframe.columns.tolist())
        self.assertEqual("Unique trajectory (identifier)", actual_dataframe.index.name)

    def test_read_csv_with_data_directory_data_camel_case(self) -> None:
        """
        Test: That read_csv produces the expected dataframe with mock data directory
         data.
        When: read_csv is called with mock data directory data and output_camel_case
         is True.
        """
        actual_dataframe = msr.read_csv(self.mock_data_directory_csv.read_text(),
                                        output_camel_case=True)

        self.assertFalse(actual_dataframe.empty)
        self.assertEqual((497, 85), actual_dataframe.shape)
        self.assertEqual(
            ["20181210010656_eBlUM", "20181210012238_ucxkx", "20181210024213_c2bJq"],
            actual_dataframe.index.tolist()[:3],
        )
        self.assertEqual(EXPECTED_DTYPES, actual_dataframe.dtypes.tolist())
        self.assertEqual(EXPECTED_COLUMN_NAMES_CAMEL_CASE, actual_dataframe.columns.tolist())
        self.assertEqual("unique_trajectory_identifier", actual_dataframe.index.name)

    def test_read_meteor_summary_csv_as_dataframe_rest_api(self) -> None:
        """
        Test: That read_csv produces the expected dataframe with mock rest api data.
        When: read_csv is called with mock rest api data.
        """
        actual_dataframe = msr.read_csv(
            self.mock_rest_api_csv.read_text(),
            rest_format=True,
        )

        self.assertFalse(actual_dataframe.empty)
        self.assertEqual((100, 85), actual_dataframe.shape)
        self.assertEqual(
            ["20220304220741_yrPTs", "20220401012310_f5I2M", "20220401012318_BIAD6"],
            actual_dataframe.index.tolist()[:3],
        )
        actual_dataframe.info()
        self.assertEqual(EXPECTED_DTYPES, actual_dataframe.dtypes.tolist())
        self.assertEqual(EXPECTED_COLUMN_NAMES, actual_dataframe.columns.tolist())
        self.assertEqual("Unique trajectory (identifier)", actual_dataframe.index.name)

        # With output_camel_case = True, the dataframe should not change because REST
        # API data is already in camel case.
        actual_dataframe_camel_case = msr.read_csv(
            self.mock_rest_api_csv.read_text(),
            rest_format=True,
            output_camel_case=True,
        )
        self.assertTrue(actual_dataframe.equals(actual_dataframe_camel_case))


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
