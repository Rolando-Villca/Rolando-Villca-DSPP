"""Illustrative weekly inflation helpers; all planning inputs must be fictional.

Observed inflation may only be used in a historical backtest after publication.
Do not apply an annual percentage as a new increase every single week.
"""
import math


def annual_to_weekly_rate(annual_rate: float, weeks_in_year: int = 52) -> float:
    """Effective weekly compounding rate from an annual decimal rate."""
    rate = float(annual_rate)
    if not math.isfinite(rate) or rate <= -1:
        raise ValueError("Annual rate must be finite and greater than -100%")
    if weeks_in_year < 1:
        raise ValueError("weeks_in_year must be positive")
    return (1 + rate)**(1/weeks_in_year) - 1


def inflate_driver(base_value: float, annual_rate: float, weeks: int) -> float:
    """Uplift one nominal AIV or ACP using a fictional constant weekly rate."""
    base = float(base_value)
    if not math.isfinite(base) or base <= 0 or weeks < 0:
        raise ValueError("Positive base value and nonnegative weeks required")
    return base * (1 + annual_to_weekly_rate(annual_rate))**weeks


def inflate_by_index(base_value: float, base_index: float, future_index: float) -> float:
    """Use an index level ratio, if the future index was actually available."""
    if not all(math.isfinite(float(v)) and float(v)>0
               for v in (base_value,base_index,future_index)):
        raise ValueError("Values and index levels must be finite and positive")
    return base_value * future_index / base_index
