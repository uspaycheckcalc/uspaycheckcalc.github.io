"""
State income tax data, tax year 2026, single filer.

Cross-checked 2026-08-22 primarily via Tax Foundation (taxfoundation.org/data/all/state/state-income-tax-rates-2026)
plus state revenue department publications for standard deduction / personal exemption amounts.
15 states chosen by population rank (top-15 by population covers the bulk of US search demand and
naturally mixes no-tax / flat-tax / progressive-tax structures). Update annually.

Each entry:
  name       - display name
  type       - "none" | "flat" | "progressive" (for UI labeling only; tax math always uses `brackets`)
  deduction  - dollar amount subtracted from gross wages before applying brackets (state standard
               deduction or personal exemption; 0 if the state has none for wage earners)
  brackets   - list of (bracket start, marginal rate) ascending, or None for no-tax states
  note       - optional caveat shown in the page disclaimer

Scope limitation (deliberate, per data-quality policy): only the state's standard deduction/personal
exemption is modeled. Other state-specific credits, local/city taxes (e.g. NYC), and itemized
deductions are NOT included - the disclaimer on generated pages says so explicitly.
"""

STATES = {
    "california": {
        "name": "California",
        "type": "progressive",
        "deduction": 5_706,
        "brackets": [
            (0, 0.01), (11_079, 0.02), (26_264, 0.04), (41_452, 0.06),
            (57_542, 0.08), (72_724, 0.093), (371_479, 0.103),
            (445_771, 0.113), (742_953, 0.123), (1_000_000, 0.133),
        ],
    },
    "texas": {
        "name": "Texas", "type": "none", "deduction": 0, "brackets": None,
    },
    "new-york": {
        "name": "New York",
        "type": "progressive",
        "deduction": 8_000,
        "brackets": [
            (0, 0.039), (8_500, 0.044), (11_700, 0.0515), (13_900, 0.054),
            (80_650, 0.059), (215_400, 0.0685), (1_077_550, 0.0965),
            (5_000_000, 0.103), (25_000_000, 0.109),
        ],
        "note": "Excludes New York City local income tax, which applies only to NYC residents.",
    },
    "florida": {
        "name": "Florida", "type": "none", "deduction": 0, "brackets": None,
    },
    "pennsylvania": {
        "name": "Pennsylvania",
        "type": "flat",
        "deduction": 0,
        "brackets": [(0, 0.0307)],
        "note": "Pennsylvania has no standard deduction or personal exemption for wage income.",
    },
    "illinois": {
        "name": "Illinois",
        "type": "flat",
        "deduction": 2_925,
        "brackets": [(0, 0.0495)],
    },
    "ohio": {
        "name": "Ohio",
        "type": "flat",
        "deduction": 0,
        "brackets": [(0, 0.0), (26_050, 0.0275)],
        "note": "Ohio moved to a flat 2.75% rate on non-business income above $26,050 starting 2026.",
    },
    "georgia": {
        "name": "Georgia",
        "type": "flat",
        "deduction": 12_000,
        "brackets": [(0, 0.0519)],
        "note": "Georgia's flat rate is on a legislated step-down schedule; sources vary slightly (5.19% used here).",
    },
    "north-carolina": {
        "name": "North Carolina",
        "type": "flat",
        "deduction": 12_750,
        "brackets": [(0, 0.0399)],
    },
    "michigan": {
        "name": "Michigan",
        "type": "flat",
        "deduction": 5_900,
        "brackets": [(0, 0.0425)],
    },
    "new-jersey": {
        "name": "New Jersey",
        "type": "progressive",
        "deduction": 1_000,
        "brackets": [
            (0, 0.014), (20_000, 0.0175), (35_000, 0.035),
            (40_000, 0.05525), (75_000, 0.0637), (500_000, 0.0897),
            (1_000_000, 0.1075),
        ],
    },
    "virginia": {
        "name": "Virginia",
        "type": "progressive",
        "deduction": 8_750,
        "brackets": [(0, 0.02), (3_000, 0.03), (5_000, 0.05), (17_000, 0.0575)],
    },
    "washington": {
        "name": "Washington", "type": "none", "deduction": 0, "brackets": None,
    },
    "arizona": {
        "name": "Arizona",
        "type": "flat",
        "deduction": 13_850,
        "brackets": [(0, 0.025)],
    },
    "massachusetts": {
        "name": "Massachusetts",
        "type": "flat",
        "deduction": 4_400,
        "brackets": [(0, 0.05), (1_083_150, 0.09)],
        "note": "The 9% rate only applies to income above $1,083,150 (the 'millionaire's tax' surtax).",
    },
}

STATE_ORDER = [
    "california", "texas", "florida", "new-york", "pennsylvania", "illinois",
    "ohio", "georgia", "north-carolina", "michigan", "new-jersey", "virginia",
    "washington", "arizona", "massachusetts",
]
