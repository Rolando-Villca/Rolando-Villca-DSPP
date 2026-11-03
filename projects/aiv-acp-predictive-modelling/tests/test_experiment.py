"""Tests for synthetic AIV/ACP backtesting and leakage checks."""
import unittest
import numpy as np
from src.experiment import (
    make_synthetic_history, backtest, planning_features, STORES, SECTORS
)


class SyntheticBacktestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.panel=make_synthetic_history()
        cls.test,cls.results=backtest(cls.panel)

    def test_all_identifiers_are_fictional(self):
        self.assertTrue(self.panel.store_id.str.startswith("DEMO-STORE-").all())
        self.assertTrue(self.panel.sector_id.str.startswith("CATEGORY-").all())

    def test_training_and_q1_2026_holdout_are_chronological(self):
        self.assertEqual(self.results["scope"]["training_rows"],
                         len(STORES)*len(SECTORS)*52*4)
        self.assertEqual(self.results["scope"]["holdout_rows"],
                         len(STORES)*len(SECTORS)*13)
        self.assertEqual(
            sorted(self.test.week.unique().tolist()),list(range(1,14))
        )

    def test_historical_ratios_reconstruct_quantities(self):
        h=self.panel
        self.assertTrue(np.allclose(
            h.sector_actual_sales/h.AIV_actual,h.items_actual))
        self.assertTrue(np.allclose(
            h.sector_actual_sales/h.ACP_actual,h.cases_actual))

    def test_identical_sales_forecast_for_both_methods(self):
        t=self.test
        for method in ("static","model"):
            self.assertTrue(np.allclose(
                t[f"items_{method}"]*t[f"AIV_{method}"],
                t.sector_forecast_sales))
            self.assertTrue(np.allclose(
                t[f"cases_{method}"]*t[f"ACP_{method}"],
                t.sector_forecast_sales))

    def test_features_exclude_future_actuals_and_inflation(self):
        features=planning_features(self.test)
        self.assertFalse(any("actual" in c for c in features.columns))
        self.assertFalse(any("inflation" in c for c in features.columns))

    def test_hours_match_units_times_smv(self):
        t=self.test
        self.assertTrue(np.allclose(
            t.hours_actual,t.actual_task_units*t.SMV_minutes_per_unit/60))
        for method in ("static","model"):
            self.assertTrue(np.allclose(
                t[f"hours_{method}"],
                t[f"task_units_{method}"]*t.SMV_minutes_per_unit/60))

    def test_fixed_random_seed(self):
        again=make_synthetic_history()
        self.assertTrue(np.allclose(self.panel.AIV_actual,again.AIV_actual))


if __name__ == "__main__":
    unittest.main()
