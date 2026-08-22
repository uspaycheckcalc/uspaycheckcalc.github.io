"""
Generates all pages for the US Paycheck Calculator site:
  - index.html            national live calculator + links to all 15 state hub pages
  - {state}.html           per-state hub: live calculator preset to that state + links to its salary presets
  - {state}-{N}k-paycheck-calculator.html   static preset detail page for one state+salary combo

Programmatic-SEO scope: 15 states (by population rank) x 14 salary points ($20k-$150k, $10k steps) =
210 detail pages, matching real search patterns (round salary numbers) rather than dense presets.
"""
import json
import os

from calc import calculate
from state_data import STATES, STATE_ORDER
import federal_data
from static_pages import (
    about_html, privacy_html, contact_html,
    SITE_NAME, GA_SNIPPET, FOOTER_NAV, SITE_STYLE, SITE_HEADER, FAVICON,
)

OUTPUT_DIR = "docs"
BASE_URL = "https://uspaycheckcalc.github.io"

SALARY_START = 20_000
SALARY_END = 150_000
SALARY_STEP = 10_000
SALARIES = list(range(SALARY_START, SALARY_END + 1, SALARY_STEP))


def fmt(n):
    return f"{n:,.0f}"


def state_slug(state_key):
    return f"{state_key}.html"


def detail_slug(state_key, salary):
    return f"{state_key}-{salary // 1000}k-paycheck-calculator.html"


# ---- client-side calculator JS (mirrors calc.py) ----
def build_calc_js():
    states_js = {
        key: {"name": s["name"], "deduction": s["deduction"], "brackets": s["brackets"] or []}
        for key, s in STATES.items()
    }
    return f"""
const FEDERAL_STD_DEDUCTION = {federal_data.STANDARD_DEDUCTION};
const FEDERAL_BRACKETS = {json.dumps(federal_data.BRACKETS)};
const SS_RATE = {federal_data.SOCIAL_SECURITY_RATE}, SS_WAGE_BASE = {federal_data.SOCIAL_SECURITY_WAGE_BASE};
const MEDICARE_RATE = {federal_data.MEDICARE_RATE}, ADDL_MEDICARE_RATE = {federal_data.ADDITIONAL_MEDICARE_RATE};
const ADDL_MEDICARE_THRESHOLD = {federal_data.ADDITIONAL_MEDICARE_THRESHOLD_SINGLE};
const STATES = {json.dumps(states_js)};

function bracketTax(taxable, brackets) {{
  if (taxable <= 0 || !brackets.length) return 0;
  let tax = 0;
  for (let i = 0; i < brackets.length; i++) {{
    const [start, rate] = brackets[i];
    const upper = i + 1 < brackets.length ? brackets[i + 1][0] : Infinity;
    if (taxable > start) tax += (Math.min(taxable, upper) - start) * rate;
    else break;
  }}
  return tax;
}}

function calculatePaycheck(gross, stateKey) {{
  const fedTax = bracketTax(Math.max(gross - FEDERAL_STD_DEDUCTION, 0), FEDERAL_BRACKETS);
  const ss = Math.min(gross, SS_WAGE_BASE) * SS_RATE;
  let medicare = gross * MEDICARE_RATE;
  if (gross > ADDL_MEDICARE_THRESHOLD) medicare += (gross - ADDL_MEDICARE_THRESHOLD) * ADDL_MEDICARE_RATE;
  const state = STATES[stateKey];
  const stateTax = bracketTax(Math.max(gross - state.deduction, 0), state.brackets);
  const totalTax = fedTax + ss + medicare + stateTax;
  const netAnnual = gross - totalTax;
  return {{ fedTax, ss, medicare, stateTax, totalTax, netAnnual, netMonthly: netAnnual / 12 }};
}}

function fmtUSD(n) {{ return '$' + Math.round(n).toLocaleString('en-US'); }}

function calc(defaultState) {{
  const salaryEl = document.getElementById('salary');
  const stateEl = document.getElementById('state');
  const salary = parseFloat(salaryEl.value) || 0;
  const stateKey = stateEl ? stateEl.value : defaultState;
  if (salary <= 0) return;
  const r = calculatePaycheck(salary, stateKey);
  document.getElementById('r-federal').textContent = fmtUSD(r.fedTax);
  document.getElementById('r-state').textContent = fmtUSD(r.stateTax);
  document.getElementById('r-ss').textContent = fmtUSD(r.ss);
  document.getElementById('r-medicare').textContent = fmtUSD(r.medicare);
  document.getElementById('r-net-annual').textContent = fmtUSD(r.netAnnual);
  document.getElementById('r-net-monthly').textContent = fmtUSD(r.netMonthly);
}}
"""


CALC_JS = build_calc_js()


def calculator_box_html(default_state_key, fixed_state=False):
    if fixed_state:
        state_field = f'<input type="hidden" id="state" value="{default_state_key}">'
    else:
        options = "\n".join(
            f'<option value="{key}"{" selected" if key == default_state_key else ""}>{STATES[key]["name"]}</option>'
            for key in STATE_ORDER
        )
        state_field = f"""<div class="field">
      <label for="state">State</label>
      <select id="state" onchange="calc('{default_state_key}')">{options}</select>
    </div>"""

    return f"""<div class="calc-box">
    {state_field}
    <div class="field">
      <label for="salary">Annual salary (gross, $)</label>
      <input type="number" id="salary" placeholder="e.g. 75000" oninput="calc('{default_state_key}')">
    </div>
    <div class="result">
      <div class="result-row"><span>Federal income tax</span><span id="r-federal">-</span></div>
      <div class="result-row"><span>State income tax</span><span id="r-state">-</span></div>
      <div class="result-row"><span>Social Security</span><span id="r-ss">-</span></div>
      <div class="result-row"><span>Medicare</span><span id="r-medicare">-</span></div>
      <div class="result-row total"><span>Net pay (annual)</span><span id="r-net-annual">-</span></div>
      <div class="result-row"><span>Net pay (monthly)</span><span id="r-net-monthly">-</span></div>
    </div>
  </div>"""


DISCLAIMER = """
  <div class="disclaimer">
    * Estimates assume a single filer taking the standard deduction, with no dependents, credits,
    or additional withholding, for the 2026 tax year. Local/city income taxes (e.g. New York City)
    and other state-specific credits are not included. Federal and state tax rates change over
    time - see the About page for details and check a recent pay stub or a tax professional for
    exact figures.
  </div>
"""


def page_shell(title, description, body, extra_head=""):
    return f"""<!doctype html>
<html lang="en">
<head>
{GA_SNIPPET}
<meta charset="utf-8">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="viewport" content="width=device-width, initial-scale=1">
{FAVICON}
{extra_head}
<style>{SITE_STYLE}</style>
</head>
<body>
{SITE_HEADER}
{body}
{FOOTER_NAV}
<script>
{CALC_JS}
</script>
</body>
</html>"""


def index_html():
    state_links = "\n".join(
        f'<li><a href="{state_slug(key)}">{STATES[key]["name"]}</a></li>' for key in STATE_ORDER
    )
    body = f"""
  <h1>US Paycheck Calculator</h1>
  <p>Estimate your take-home pay after federal tax, Social Security, Medicare, and state income tax.
  Pick a state and enter your gross annual salary below.</p>

  {calculator_box_html("california")}

  <h2>Browse by state</h2>
  <ul class="division-list">
  {state_links}
  </ul>

  <div class="explain">
    <h2>What's included</h2>
    <p>This calculator covers the 15 most populous US states, including the nine states with no
    wage income tax (Texas, Florida, Washington, and others) alongside flat-tax and progressive-tax
    states. See each state's page for salary-specific breakdowns.</p>
  </div>
{DISCLAIMER}
"""
    return page_shell(
        f"{SITE_NAME} - Estimate Your Take-Home Pay by State",
        "Free US paycheck calculator: estimate take-home pay after federal tax, FICA, and state income tax for 15 major states.",
        body,
    )


def state_hub_html(state_key):
    state = STATES[state_key]
    salary_links = "\n".join(
        f'<li><a href="{detail_slug(state_key, s)}">${s // 1000}k salary</a></li>' for s in SALARIES
    )
    tax_type_desc = {
        "none": f"{state['name']} has no state income tax on wages.",
        "flat": f"{state['name']} applies a flat state income tax rate.",
        "progressive": f"{state['name']} applies a progressive (bracketed) state income tax.",
    }[state["type"]]

    note_html = f'<p class="source">{state["note"]}</p>' if state.get("note") else ""

    body = f"""
  <h1>{state['name']} Paycheck Calculator</h1>
  <p>{tax_type_desc} Enter your gross annual salary to estimate your {state['name']} take-home pay.</p>

  {calculator_box_html(state_key, fixed_state=True)}
  {note_html}

  <h2>Common salaries in {state['name']}</h2>
  <ul class="division-list">
  {salary_links}
  </ul>

  <div class="nav"><a href="index.html">&larr; All states</a></div>
{DISCLAIMER}
"""
    return page_shell(
        f"{state['name']} Paycheck Calculator - Take-Home Pay by Salary (2026)",
        f"Estimate take-home pay in {state['name']} after federal tax, FICA, and state income tax. See common salary breakdowns from $20k to $150k.",
        body,
    )


def detail_html(state_key, salary, prev_salary, next_salary):
    state = STATES[state_key]
    r = calculate(salary, state_key)
    title = f"${salary:,} Salary {state['name']} Paycheck Calculator - ${fmt(r['net_monthly'])}/mo Take-Home (2026)"
    desc = f"${salary:,} gross salary in {state['name']} nets about ${fmt(r['net_monthly'])}/month after federal tax, FICA, and state tax."

    nav_links = []
    if prev_salary:
        nav_links.append(f'<a href="{detail_slug(state_key, prev_salary)}">&larr; ${prev_salary // 1000}k</a>')
    if next_salary:
        nav_links.append(f'<a href="{detail_slug(state_key, next_salary)}">${next_salary // 1000}k &rarr;</a>')
    nav_html = " | ".join(nav_links)

    body = f"""
  <h1>${salary:,} Salary in {state['name']}: Paycheck Breakdown</h1>
  <div class="headline">
    <div>Take-home pay on a ${salary:,} salary in {state['name']}</div>
    <div class="amount">${fmt(r['net_monthly'])}/mo</div>
    <div>(${fmt(r['net_annual'])}/year, ${fmt(r['net_biweekly'])} per biweekly paycheck)</div>
  </div>

  <table>
    <tr><th>Deduction</th><th>Annual amount</th></tr>
    <tr><td>Federal income tax</td><td>${fmt(r['federal_tax'])}</td></tr>
    <tr><td>State income tax ({state['name']})</td><td>${fmt(r['state_tax'])}</td></tr>
    <tr><td>Social Security</td><td>${fmt(r['social_security'])}</td></tr>
    <tr><td>Medicare</td><td>${fmt(r['medicare'])}</td></tr>
    <tr><th>Total tax</th><th>${fmt(r['total_tax'])}</th></tr>
  </table>

  <div class="nav">{nav_html}</div>

  <div class="explain">
    <h2>How this is calculated</h2>
    <ol class="steps">
      <li>Federal taxable income = ${salary:,} &minus; ${fmt(federal_data.STANDARD_DEDUCTION)} standard deduction</li>
      <li>Federal income tax (2026 brackets, single filer) = <b>${fmt(r['federal_tax'])}</b></li>
      <li>Social Security (6.2%, up to the ${fmt(federal_data.SOCIAL_SECURITY_WAGE_BASE)} wage base) = <b>${fmt(r['social_security'])}</b></li>
      <li>Medicare (1.45%{f", plus 0.9% above $200,000" if salary > 200_000 else ""}) = <b>${fmt(r['medicare'])}</b></li>
      <li>{state['name']} state income tax = <b>${fmt(r['state_tax'])}</b></li>
      <li>Take-home pay = ${salary:,} &minus; ${fmt(r['total_tax'])} total tax = <b>${fmt(r['net_annual'])}/year</b></li>
    </ol>
  </div>

  <div class="nav"><a href="{state_slug(state_key)}">&larr; More {state['name']} salaries</a> | <a href="index.html">All states</a></div>
{DISCLAIMER}
"""
    return page_shell(title, desc, body)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    valid_filenames = {"index.html", "about.html", "privacy.html", "contact.html", "sitemap.xml", "ads.txt"}
    for key in STATE_ORDER:
        valid_filenames.add(state_slug(key))
        for s in SALARIES:
            valid_filenames.add(detail_slug(key, s))
    for fname in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, fname)
        if os.path.isfile(path) and fname.endswith(".html") and fname not in valid_filenames:
            os.remove(path)

    urls = []

    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html())
    urls.append(f"{BASE_URL}/index.html")

    for key in STATE_ORDER:
        with open(os.path.join(OUTPUT_DIR, state_slug(key)), "w", encoding="utf-8") as f:
            f.write(state_hub_html(key))
        urls.append(f"{BASE_URL}/{state_slug(key)}")

        for i, salary in enumerate(SALARIES):
            prev_s = SALARIES[i - 1] if i > 0 else None
            next_s = SALARIES[i + 1] if i < len(SALARIES) - 1 else None
            fname = detail_slug(key, salary)
            with open(os.path.join(OUTPUT_DIR, fname), "w", encoding="utf-8") as f:
                f.write(detail_html(key, salary, prev_s, next_s))
            urls.append(f"{BASE_URL}/{fname}")

    static_files = {"about.html": about_html(), "privacy.html": privacy_html(), "contact.html": contact_html()}
    for filename, html in static_files.items():
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(html)
        urls.append(f"{BASE_URL}/{filename}")

    print(f"Generated {len(urls)} pages -> {OUTPUT_DIR}/")
    return urls


if __name__ == "__main__":
    main()
