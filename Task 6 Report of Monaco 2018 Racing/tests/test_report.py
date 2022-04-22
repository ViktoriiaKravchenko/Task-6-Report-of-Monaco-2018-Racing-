import unittest
from unittest.mock import patch, mock_open, MagicMock, Mock
from reports import *


class TestClass(unittest.TestCase):
    @patch("reports.report.open", new_callable=mock_open,
           read_data="DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER")
    def test_read_data_from_file(self, mocked_open):
        result = read_data_from_file(["--files", "mock\\path"])
        self.assertEqual(result, ["DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER"])

    def test_abbreviation_file_list(self):
        result = abbreviation_file_list(["DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER"])
        self.assertEqual(result, [['DRR', 'Daniel Ricciardo', 'RED BULL RACING TAG HEUER']])

    def test_time_file_list(self):
        result = time_file_list(["SVF2018-05-24_12:02:58.917"])
        self.assertEqual(result, [['SVF', '2018-05-24', '12:02:58.917']])

    def test_count_time(self):
        result = count_time([['NHR', '2018-05-24', '12:02:49.914']], [['NHR', '2018-05-24', '1:04:02.979']])
        self.assertEqual(result, [['NHR', datetime.timedelta(seconds=3673, microseconds=65000)]])

    def test_built_report_desc(self):
        delta_times = [['PGS', datetime.timedelta(seconds=3672, microseconds=941000)],
                       ['NHR', datetime.timedelta(seconds=3673, microseconds=65000)]]
        racers = [['PGS', 'Pierre Gasly', 'SCUDERIA TORO ROSSO HONDA'], ['NHR', 'Nico Hulkenberg', 'RENAULT']]

        desc_parser = MagicMock()

        desc_parser.driver = False
        desc_parser.desc = True

        result = [['Nico Hulkenberg', 'RENAULT',
                   datetime.timedelta(seconds=3673, microseconds=65000)],
                  ['Pierre Gasly', 'SCUDERIA TORO ROSSO HONDA',
                   datetime.timedelta(seconds=3672, microseconds=941000)]]

        self.assertEqual(built_report(delta_times, racers, desc_parser), result)

    def test_built_report_asc(self):
        delta_times = [['PGS', datetime.timedelta(seconds=3672, microseconds=941000)],
                       ['NHR', datetime.timedelta(seconds=3673, microseconds=65000)]]
        racers = [['PGS', 'Pierre Gasly', 'SCUDERIA TORO ROSSO HONDA'], ['NHR', 'Nico Hulkenberg', 'RENAULT']]

        asc_parser = MagicMock()
        asc_parser.driver = False
        asc_parser.desc = False

        result = [['Pierre Gasly', 'SCUDERIA TORO ROSSO HONDA',
                   datetime.timedelta(seconds=3672, microseconds=941000)],
                  ['Nico Hulkenberg', 'RENAULT',
                   datetime.timedelta(seconds=3673, microseconds=65000)]]

        self.assertEqual(built_report(delta_times, racers, asc_parser), result)

    def test_built_report_driver(self):
        delta_times = [['PGS', datetime.timedelta(seconds=3672, microseconds=941000)],
                       ['NHR', datetime.timedelta(seconds=3673, microseconds=65000)]]

        racers = [['CSR', 'Carlos Sainz', 'RENAULT'], ['NHR', 'Nico Hulkenberg', 'RENAULT']]

        driver_parser = MagicMock()
        driver_parser.driver = "Nico Hulkenberg"

        result = [['Nico Hulkenberg', 'RENAULT', datetime.timedelta(seconds=3673, microseconds=65000)]]

        self.assertEqual(built_report(delta_times, racers, driver_parser), result)

    def test_main(self):
        mock = Mock()
        mock.read_data_from_file("KRF2018-05-24_12:03:01.250")
        mock.read_data_from_file.assert_called_with("KRF2018-05-24_12:03:01.250")

        mock.time_file_list("KRF2018-05-24_12:03:01.250")
        mock.time_file_list.assert_called_with("KRF2018-05-24_12:03:01.250")

        mock.count_time("KRF2018-05-24_12:03:01.250", "KRF2018-05-24_12:03:01.250")
        mock.count_time.assert_called_once_with("KRF2018-05-24_12:03:01.250", "KRF2018-05-24_12:03:01.250")

        mock.built_report()
        mock.built_report.assert_called_once()

        mock.print_report()
        mock.print_report.assert_called_once()


if __name__ == "__main__":
    unittest.main()
