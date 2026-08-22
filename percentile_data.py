"""
Income comparison data.

Scope note (deliberate): a true per-state individual-income percentile curve would require
Census ACS PUMS microdata analysis, which is out of scope here, and the readily available
per-state "median individual income" figures mix incompatible population definitions (all
persons 15+ with any income vs. full-time year-round workers only) across sources - mixing
them with the national curve below would silently misstate results. So this site provides:

  1. A NATIONAL individual-income percentile curve (single consistent source: Census/CPS ASEC
     2025 release, workforce participants 16+, all income types, cross-checked 2026-08-22).
  2. A per-state comparison against median HOUSEHOLD income (single consistent source: Census
     ACS 2023 1-year estimates) - explicitly labeled as household income, not a percentile-
     within-state claim, so the two are never conflated.
"""

# (percentile, annual income at/below which this percentile falls), ascending.
# Source: Census Bureau CPS ASEC 2025 (income year 2024), workforce participants 16+.
NATIONAL_INCOME_PERCENTILES = [
    (10, 11_005), (20, 24_054), (25, 30_000), (30, 34_001), (40, 43_345),
    (50, 53_010), (60, 65_351), (70, 81_361), (75, 93_400), (80, 106_500),
    (90, 155_042), (95, 210_351), (99, 450_100),
]

# Median household income by state, 2023 ACS 1-year estimates (inflation-adjusted dollars).
STATE_MEDIAN_HOUSEHOLD_INCOME = {
    "california": 95_521,
    "texas": 75_780,
    "florida": 73_311,
    "new-york": 82_095,
    "pennsylvania": 73_824,
    "illinois": 80_306,
    "ohio": 67_769,
    "georgia": 74_632,
    "north-carolina": 70_804,
    "michigan": 69_183,
    "new-jersey": 99_781,
    "virginia": 89_931,
    "washington": 94_605,
    "arizona": 77_315,
    "massachusetts": 99_858,
}
