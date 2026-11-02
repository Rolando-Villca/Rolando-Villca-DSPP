import unittest

from src.workload import (
    sector_sales, items_from_aiv, cases_from_acp, cases_from_items,
    task_hours, example,
)


class WorkloadLogicTests(unittest.TestCase):
    def test_sector_sales_uses_mix(self):
        self.assertEqual(sector_sales(120_000, .25), 30_000)

    def test_aiv_items_then_cases(self):
        self.assertEqual(items_from_aiv(30_000, 5), 6_000)
        self.assertEqual(cases_from_items(6_000, 12), 500)

    def test_acp_is_alternative_path(self):
        self.assertEqual(cases_from_acp(30_000, 60), 500)
        self.assertEqual(example()["case_task_hours"], 20)

    def test_quarterly_driver_changes_derived_hours(self):
        annual_hours = task_hours(cases_from_acp(30_000, 60), 2.4)
        quarterly_hours = task_hours(cases_from_acp(30_000, 75), 2.4)
        self.assertEqual(annual_hours - quarterly_hours, 4)

    def test_invalid_mix(self):
        with self.assertRaises(ValueError):
            sector_sales(10, 1.5)

    def test_invalid_driver(self):
        with self.assertRaises(ValueError):
            items_from_aiv(10, 0)


if __name__ == "__main__":
    unittest.main()
