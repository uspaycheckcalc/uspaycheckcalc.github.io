"""
US paycheck (take-home pay) calculation logic, tax year 2026.

Model: single filer, standard deduction only, no dependents/credits (same simplification
precedent as the KR salary-calculator project). See federal_data.py / state_data.py for the
underlying rates and their sources - both must be refreshed annually.
"""
import federal_data
from state_data import STATES


def bracket_tax(taxable, brackets):
    """Marginal-bracket tax. `brackets` is an ascending list of (bracket_start, rate)."""
    if taxable <= 0 or not brackets:
        return 0
    tax = 0.0
    for i, (start, rate) in enumerate(brackets):
        upper = brackets[i + 1][0] if i + 1 < len(brackets) else float("inf")
        if taxable > start:
            tax += (min(taxable, upper) - start) * rate
        else:
            break
    return tax


def federal_tax(gross_annual):
    taxable = max(gross_annual - federal_data.STANDARD_DEDUCTION, 0)
    return bracket_tax(taxable, federal_data.BRACKETS)


def fica(gross_annual):
    ss = min(gross_annual, federal_data.SOCIAL_SECURITY_WAGE_BASE) * federal_data.SOCIAL_SECURITY_RATE
    medicare = gross_annual * federal_data.MEDICARE_RATE
    if gross_annual > federal_data.ADDITIONAL_MEDICARE_THRESHOLD_SINGLE:
        medicare += (gross_annual - federal_data.ADDITIONAL_MEDICARE_THRESHOLD_SINGLE) * federal_data.ADDITIONAL_MEDICARE_RATE
    return ss, medicare


def state_tax(gross_annual, state_key):
    state = STATES[state_key]
    if state["brackets"] is None:
        return 0
    taxable = max(gross_annual - state["deduction"], 0)
    return bracket_tax(taxable, state["brackets"])


def calculate(gross_annual: float, state_key: str) -> dict:
    fed_tax = federal_tax(gross_annual)
    ss, medicare = fica(gross_annual)
    st_tax = state_tax(gross_annual, state_key)

    total_tax = fed_tax + ss + medicare + st_tax
    net_annual = gross_annual - total_tax

    return {
        "gross_annual": round(gross_annual),
        "federal_tax": round(fed_tax),
        "social_security": round(ss),
        "medicare": round(medicare),
        "state_tax": round(st_tax),
        "total_tax": round(total_tax),
        "net_annual": round(net_annual),
        "net_monthly": round(net_annual / 12),
        "net_biweekly": round(net_annual / 26),
    }


if __name__ == "__main__":
    for state_key in ["california", "texas", "pennsylvania", "ohio", "new-york"]:
        for salary in [50_000, 75_000, 120_000]:
            r = calculate(salary, state_key)
            print(
                f"{STATES[state_key]['name']:<12} ${salary:,} -> "
                f"net ${r['net_annual']:,}/yr (${r['net_monthly']:,}/mo), "
                f"tax breakdown: fed ${r['federal_tax']:,} state ${r['state_tax']:,} "
                f"SS ${r['social_security']:,} medicare ${r['medicare']:,}"
            )
