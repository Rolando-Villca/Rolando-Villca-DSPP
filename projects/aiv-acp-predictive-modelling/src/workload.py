"""A deliberately simplified, synthetic demonstration of workload conversions.

Not an operational labour-planning model. Inputs must be fictional or approved for sharing.
"""


def _positive(value: float, label: str) -> float:
    value = float(value)
    if not 0 < value < float("inf"):
        raise ValueError(f"{label} must be finite and positive")
    return value


def sector_sales(division_sales: float, sector_mix: float) -> float:
    """Allocate division sales to one product sector using a fractional mix."""
    sales = float(division_sales)
    mix = float(sector_mix)
    if not 0 <= sales < float("inf"):
        raise ValueError("division_sales must be finite and nonnegative")
    if not 0 <= mix <= 1:
        raise ValueError("sector_mix must be between zero and one")
    return sales * mix


def items_from_aiv(sales: float, aiv: float) -> float:
    return float(sales) / _positive(aiv, "AIV")


def cases_from_acp(sales: float, acp: float) -> float:
    return float(sales) / _positive(acp, "ACP")


def cases_from_items(items: float, items_per_case: float) -> float:
    return float(items) / _positive(items_per_case, "items per case")


def task_hours(units: float, minutes_per_unit: float) -> float:
    """Convert correctly matched task units and minutes per unit into hours."""
    if float(units) < 0:
        raise ValueError("units must be nonnegative")
    return float(units) * _positive(minutes_per_unit, "minutes per unit") / 60


def example() -> dict[str, float]:
    """Entirely fictional, equivalent alternative paths to case-based hours."""
    sales = sector_sales(120_000, 0.25)
    items = items_from_aiv(sales, 5)
    cases_by_items = cases_from_items(items, 12)
    cases_by_acp = cases_from_acp(sales, 60)
    return {
        "fictional_sector_sales_gbp": sales,
        "items_from_aiv": items,
        "cases_via_ipc": cases_by_items,
        "cases_from_acp": cases_by_acp,
        "case_task_hours": task_hours(cases_by_acp, 2.4),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(example(), indent=2))
