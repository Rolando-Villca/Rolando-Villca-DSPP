"""Tests cover synthetic identifiers, split and seven-day lag safety."""
import unittest

import numpy as np
import pandas as pd

from src.synthetic_data import generate_synthetic_demand
from src.forecast import engineer_features, chronological_split, metrics


class ForecastTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.panel = generate_synthetic_demand(n_stores=2, n_items=3, n_days=84)
        cls.frame = engineer_features(cls.panel)

    def test_identifiers_are_fictional(self):
        self.assertTrue(self.panel["store_id"].str.match(r"^DEMO-STORE-\d{3}$").all())
        self.assertTrue(self.panel["item_id"].str.match(r"^DEMO-ITEM-\d{3}$").all())

    def test_panel_has_expected_daily_grain(self):
        self.assertEqual(len(self.panel), 2 * 3 * 84)
        self.assertFalse(self.panel.duplicated(["date", "store_id", "item_id"]).any())

    def test_lag_7_is_seven_days_old(self):
        source = self.panel.query("store_id == 'DEMO-STORE-001' and item_id == 'DEMO-ITEM-001'").sort_values("date")
        target_date = source.iloc[45]["date"]
        row = self.frame.loc[
            (self.frame["store_id"] == "DEMO-STORE-001")
            & (self.frame["item_id"] == "DEMO-ITEM-001")
            & (self.frame["date"] == target_date)
        ].iloc[0]
        self.assertEqual(row["lag_7"], source.iloc[38]["units"])

    def test_rolling_mean_excludes_last_six_days(self):
        source = self.panel.query("store_id == 'DEMO-STORE-001' and item_id == 'DEMO-ITEM-001'").sort_values("date")
        target_date = source.iloc[45]["date"]
        row = self.frame.loc[
            (self.frame["store_id"] == "DEMO-STORE-001")
            & (self.frame["item_id"] == "DEMO-ITEM-001")
            & (self.frame["date"] == target_date)
        ].iloc[0]
        expected = source.iloc[32:39]["units"].mean()  # t-13 through t-7 inclusive
        self.assertAlmostEqual(row["prior_week_mean"], expected)

    def test_test_data_follows_training_data(self):
        train, test = chronological_split(self.frame, test_days=14)
        self.assertLess(train["date"].max(), test["date"].min())
        self.assertEqual(test["date"].nunique(), 14)

    def test_metrics_zero_error(self):
        m = metrics(np.array([1, 2, 3]), np.array([1, 2, 3]))
        self.assertEqual(m["MAE"], 0.0)
        self.assertEqual(m["WAPE_pct"], 0.0)


if __name__ == "__main__":
    unittest.main()
