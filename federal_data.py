"""
Federal tax data, tax year 2026 (single filer, standard deduction, no dependents).

Sources cross-checked 2026-08-22 via Tax Foundation (taxfoundation.org/data/all/federal/2026-tax-brackets)
and IRS Rev. Proc. 2025-32 inflation adjustments. Update annually when the IRS releases new figures.
"""

TAX_YEAR = 2026

STANDARD_DEDUCTION = 16_100

# (bracket start, marginal rate) ascending, single filer
BRACKETS = [
    (0, 0.10),
    (12_400, 0.12),
    (50_400, 0.22),
    (105_700, 0.24),
    (201_775, 0.32),
    (256_225, 0.35),
    (640_600, 0.37),
]

# FICA (flat, employee share)
SOCIAL_SECURITY_RATE = 0.062
SOCIAL_SECURITY_WAGE_BASE = 184_500

MEDICARE_RATE = 0.0145
ADDITIONAL_MEDICARE_RATE = 0.009
ADDITIONAL_MEDICARE_THRESHOLD_SINGLE = 200_000
