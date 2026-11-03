import unittest
from src.inflation import (
    annual_to_weekly_rate, inflate_driver, inflate_by_index
)
from src.experiment import (
    FINANCE_2025_ANNUAL_ASSUMPTION, FINANCE_2026_ANNUAL_ASSUMPTION
)


class InflationTests(unittest.TestCase):
    def test_compounding_weekly_recovers_annual(self):
        self.assertAlmostEqual((1+annual_to_weekly_rate(.04))**52,1.04)

    def test_annual_rate_is_not_applied_in_full_each_week(self):
        self.assertLess(inflate_driver(60,.028,13),60*1.028)

    def test_index_scaling(self):
        self.assertEqual(inflate_by_index(40,100,110),44)

    def test_finance_inputs_are_explicitly_fictional(self):
        self.assertAlmostEqual(FINANCE_2025_ANNUAL_ASSUMPTION,.026)
        self.assertAlmostEqual(FINANCE_2026_ANNUAL_ASSUMPTION,.028)


if __name__ == "__main__":
    unittest.main()
