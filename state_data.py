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

    # ---- Remaining 35 states, added 2026-08-22 to give the state map full US coverage ----
    # Same sourcing/methodology as above (Tax Foundation 2026 tables, deduction subtracted before
    # brackets applied). A few states conform to the federal standard deduction ($16,100) rather
    # than having their own - flagged per-state below; keep these in sync if federal_data.py changes.
    "alabama": {
        "name": "Alabama", "type": "progressive", "deduction": 3_000,
        "brackets": [(0, 0.02), (500, 0.04), (3_000, 0.05)],
    },
    "alaska": {"name": "Alaska", "type": "none", "deduction": 0, "brackets": None},
    "arkansas": {
        "name": "Arkansas", "type": "progressive", "deduction": 2_470,
        "brackets": [(0, 0.02), (4_600, 0.039)],
    },
    "colorado": {
        "name": "Colorado", "type": "flat", "deduction": 16_100,
        "brackets": [(0, 0.044)],
        "note": "Colorado conforms to the federal standard deduction.",
    },
    "connecticut": {
        "name": "Connecticut", "type": "progressive", "deduction": 15_000,
        "brackets": [
            (0, 0.02), (10_000, 0.045), (50_000, 0.055), (100_000, 0.06),
            (200_000, 0.065), (250_000, 0.069), (500_000, 0.0699),
        ],
    },
    "delaware": {
        "name": "Delaware", "type": "progressive", "deduction": 3_250,
        "brackets": [
            (0, 0.0), (2_000, 0.022), (5_000, 0.039), (10_000, 0.048),
            (20_000, 0.052), (25_000, 0.0555), (60_000, 0.066),
        ],
    },
    "hawaii": {
        "name": "Hawaii", "type": "progressive", "deduction": 4_400,
        "brackets": [
            (0, 0.014), (9_600, 0.032), (14_400, 0.055), (19_200, 0.064),
            (24_000, 0.068), (36_000, 0.072), (48_000, 0.076), (125_000, 0.079),
            (175_000, 0.0825), (225_000, 0.09), (275_000, 0.10), (325_000, 0.11),
        ],
    },
    "idaho": {
        "name": "Idaho", "type": "flat", "deduction": 16_100,
        "brackets": [(0, 0.053)],
        "note": "Idaho conforms to the federal standard deduction.",
    },
    "indiana": {
        "name": "Indiana", "type": "flat", "deduction": 1_000,
        "brackets": [(0, 0.0295)],
    },
    "iowa": {
        "name": "Iowa", "type": "flat", "deduction": 16_100,
        "brackets": [(0, 0.038)],
        "note": "Iowa conforms to the federal standard deduction.",
    },
    "kansas": {
        "name": "Kansas", "type": "progressive", "deduction": 9_160,
        "brackets": [(0, 0.052), (23_000, 0.0558)],
    },
    "kentucky": {
        "name": "Kentucky", "type": "flat", "deduction": 3_360,
        "brackets": [(0, 0.035)],
    },
    "louisiana": {
        "name": "Louisiana", "type": "flat", "deduction": 12_875,
        "brackets": [(0, 0.03)],
    },
    "maine": {
        "name": "Maine", "type": "progressive", "deduction": 8_350,
        "brackets": [(0, 0.058), (27_399, 0.0675), (64_849, 0.0715)],
    },
    "maryland": {
        "name": "Maryland", "type": "progressive", "deduction": 3_350,
        "brackets": [
            (0, 0.02), (1_000, 0.03), (2_000, 0.04), (3_000, 0.0475),
            (100_000, 0.05), (125_000, 0.0525), (150_000, 0.055),
            (250_000, 0.0575), (500_000, 0.0625), (1_000_000, 0.065),
        ],
    },
    "minnesota": {
        "name": "Minnesota", "type": "progressive", "deduction": 15_300,
        "brackets": [(0, 0.0535), (33_310, 0.068), (109_430, 0.0785), (203_150, 0.0985)],
    },
    "mississippi": {
        "name": "Mississippi", "type": "flat", "deduction": 2_300,
        "brackets": [(0, 0.0), (10_000, 0.04)],
    },
    "missouri": {
        "name": "Missouri", "type": "progressive", "deduction": 16_100,
        "brackets": [
            (0, 0.0), (1_348, 0.02), (2_696, 0.025), (4_044, 0.03),
            (5_392, 0.035), (6_740, 0.04), (8_088, 0.045), (9_436, 0.047),
        ],
        "note": "Missouri conforms to the federal standard deduction.",
    },
    "montana": {
        "name": "Montana", "type": "progressive", "deduction": 16_100,
        "brackets": [(0, 0.047), (47_500, 0.0565)],
        "note": "Montana conforms to the federal standard deduction.",
    },
    "nebraska": {
        "name": "Nebraska", "type": "progressive", "deduction": 8_850,
        "brackets": [(0, 0.0246), (4_130, 0.0351), (24_760, 0.0455)],
    },
    "nevada": {"name": "Nevada", "type": "none", "deduction": 0, "brackets": None},
    "new-hampshire": {"name": "New Hampshire", "type": "none", "deduction": 0, "brackets": None},
    "new-mexico": {
        "name": "New Mexico", "type": "progressive", "deduction": 16_100,
        "brackets": [
            (0, 0.015), (5_500, 0.032), (16_500, 0.043),
            (33_500, 0.047), (66_500, 0.049), (210_000, 0.059),
        ],
        "note": "New Mexico conforms to the federal standard deduction.",
    },
    "north-dakota": {
        "name": "North Dakota", "type": "progressive", "deduction": 16_100,
        "brackets": [(0, 0.0), (48_475, 0.0195), (244_825, 0.025)],
        "note": "North Dakota conforms to the federal standard deduction; a very low-rate tax overall.",
    },
    "oklahoma": {
        "name": "Oklahoma", "type": "progressive", "deduction": 6_350,
        "brackets": [(0, 0.0), (3_750, 0.025), (4_900, 0.035), (7_200, 0.045)],
    },
    "oregon": {
        "name": "Oregon", "type": "progressive", "deduction": 2_910,
        "brackets": [(0, 0.0475), (4_550, 0.0675), (11_400, 0.0875), (125_000, 0.099)],
    },
    "rhode-island": {
        "name": "Rhode Island", "type": "progressive", "deduction": 11_200,
        "brackets": [(0, 0.0375), (82_050, 0.0475), (186_450, 0.0599)],
    },
    "south-carolina": {
        "name": "South Carolina", "type": "progressive", "deduction": 8_350,
        "brackets": [(0, 0.0), (3_640, 0.03), (18_230, 0.06)],
    },
    "south-dakota": {"name": "South Dakota", "type": "none", "deduction": 0, "brackets": None},
    "tennessee": {"name": "Tennessee", "type": "none", "deduction": 0, "brackets": None},
    "utah": {
        "name": "Utah", "type": "flat", "deduction": 0,
        "brackets": [(0, 0.045)],
        "note": "Utah uses a nonrefundable taxpayer credit rather than a standard deduction; "
                "this simplified model may modestly overstate Utah tax.",
    },
    "vermont": {
        "name": "Vermont", "type": "progressive", "deduction": 7_650,
        "brackets": [(0, 0.0335), (49_400, 0.066), (119_700, 0.076), (249_700, 0.0875)],
    },
    "west-virginia": {
        "name": "West Virginia", "type": "progressive", "deduction": 0,
        "brackets": [(0, 0.0222), (10_000, 0.0296), (25_000, 0.0333), (40_000, 0.0444), (60_000, 0.0482)],
        "note": "West Virginia's standard deduction figure was not available from the source used; "
                "this simplified model may modestly overstate WV tax at lower incomes.",
    },
    "wisconsin": {
        "name": "Wisconsin", "type": "progressive", "deduction": 13_960,
        "brackets": [(0, 0.035), (15_110, 0.044), (51_950, 0.053), (332_720, 0.0765)],
    },
    "wyoming": {"name": "Wyoming", "type": "none", "deduction": 0, "brackets": None},
}

# Curated subset shown in the "Browse by state" list (original 15, by population rank) - kept
# deliberately short so that section doesn't get cluttered. The map below covers all 50.
STATE_ORDER = [
    "california", "texas", "florida", "new-york", "pennsylvania", "illinois",
    "ohio", "georgia", "north-carolina", "michigan", "new-jersey", "virginia",
    "washington", "arizona", "massachusetts",
]

# All 50 states, alphabetical - used for the calculator's state dropdown and for generating
# every state's hub + salary-detail pages (so every map tile has a real destination).
ALL_STATE_ORDER = [
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado",
    "connecticut", "delaware", "florida", "georgia", "hawaii", "idaho",
    "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana", "maine",
    "maryland", "massachusetts", "michigan", "minnesota", "mississippi",
    "missouri", "montana", "nebraska", "nevada", "new-hampshire", "new-jersey",
    "new-mexico", "new-york", "north-carolina", "north-dakota", "ohio",
    "oklahoma", "oregon", "pennsylvania", "rhode-island", "south-carolina",
    "south-dakota", "tennessee", "texas", "utah", "vermont", "virginia",
    "washington", "west-virginia", "wisconsin", "wyoming",
]

# Tile-grid layout for the US map (12-col x 8-row cartogram, same simplified-square-state approach
# used on the usstatewages.github.io project - reused as-is rather than re-deriving coordinates).
MAP_STATES = {
    "alabama": {"abbr": "AL", "col": 7, "row": 6},
    "alaska": {"abbr": "AK", "col": 0, "row": 0},
    "arizona": {"abbr": "AZ", "col": 2, "row": 4},
    "arkansas": {"abbr": "AR", "col": 5, "row": 5},
    "california": {"abbr": "CA", "col": 1, "row": 3},
    "colorado": {"abbr": "CO", "col": 3, "row": 3},
    "connecticut": {"abbr": "CT", "col": 11, "row": 3},
    "delaware": {"abbr": "DE", "col": 10, "row": 4},
    "florida": {"abbr": "FL", "col": 8, "row": 7},
    "georgia": {"abbr": "GA", "col": 8, "row": 6},
    "hawaii": {"abbr": "HI", "col": 0, "row": 4},
    "idaho": {"abbr": "ID", "col": 2, "row": 1},
    "illinois": {"abbr": "IL", "col": 6, "row": 3},
    "indiana": {"abbr": "IN", "col": 7, "row": 3},
    "iowa": {"abbr": "IA", "col": 5, "row": 3},
    "kansas": {"abbr": "KS", "col": 4, "row": 4},
    "kentucky": {"abbr": "KY", "col": 6, "row": 4},
    "louisiana": {"abbr": "LA", "col": 5, "row": 6},
    "maine": {"abbr": "ME", "col": 11, "row": 0},
    "maryland": {"abbr": "MD", "col": 9, "row": 4},
    "massachusetts": {"abbr": "MA", "col": 10, "row": 2},
    "michigan": {"abbr": "MI", "col": 6, "row": 2},
    "minnesota": {"abbr": "MN", "col": 5, "row": 1},
    "mississippi": {"abbr": "MS", "col": 6, "row": 6},
    "missouri": {"abbr": "MO", "col": 5, "row": 4},
    "montana": {"abbr": "MT", "col": 3, "row": 1},
    "nebraska": {"abbr": "NE", "col": 4, "row": 3},
    "nevada": {"abbr": "NV", "col": 2, "row": 2},
    "new-hampshire": {"abbr": "NH", "col": 10, "row": 1},
    "new-jersey": {"abbr": "NJ", "col": 10, "row": 3},
    "new-mexico": {"abbr": "NM", "col": 3, "row": 4},
    "new-york": {"abbr": "NY", "col": 9, "row": 2},
    "north-carolina": {"abbr": "NC", "col": 7, "row": 5},
    "north-dakota": {"abbr": "ND", "col": 4, "row": 1},
    "ohio": {"abbr": "OH", "col": 8, "row": 3},
    "oklahoma": {"abbr": "OK", "col": 4, "row": 5},
    "oregon": {"abbr": "OR", "col": 1, "row": 2},
    "pennsylvania": {"abbr": "PA", "col": 9, "row": 3},
    "rhode-island": {"abbr": "RI", "col": 11, "row": 4},
    "south-carolina": {"abbr": "SC", "col": 8, "row": 5},
    "south-dakota": {"abbr": "SD", "col": 4, "row": 2},
    "tennessee": {"abbr": "TN", "col": 6, "row": 5},
    "texas": {"abbr": "TX", "col": 4, "row": 6},
    "utah": {"abbr": "UT", "col": 2, "row": 3},
    "vermont": {"abbr": "VT", "col": 9, "row": 1},
    "virginia": {"abbr": "VA", "col": 8, "row": 4},
    "washington": {"abbr": "WA", "col": 1, "row": 1},
    "west-virginia": {"abbr": "WV", "col": 7, "row": 4},
    "wisconsin": {"abbr": "WI", "col": 5, "row": 2},
    "wyoming": {"abbr": "WY", "col": 3, "row": 2},
}
