import unittest
from src.analysis import synthetic_panel, evaluate


class SyntheticProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = synthetic_panel()

    def test_all_identifiers_fictional(self):
        self.assertTrue(self.df.store_id.str.startswith("DEMO-STORE-").all())
        self.assertTrue(self.df.category.str.startswith("CATEGORY-").all())

    def test_no_duplicate_grain(self):
        self.assertFalse(self.df.duplicated(["store_id", "category", "year", "quarter"]).any())

    def test_all_values_positive(self):
        self.assertTrue((self.df[["AIV", "ACP"]] > 0).all().all())

    def test_model_has_finite_errors(self):
        for target in ("AIV", "ACP"):
            result = evaluate(self.df, target)
            self.assertGreaterEqual(result["ridge_MAE"], 0)
            self.assertGreaterEqual(result["historical_baseline_MAE"], 0)


if __name__ == "__main__":
    unittest.main()
