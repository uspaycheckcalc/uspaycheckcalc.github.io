"""
Generates all pages for the US Paycheck Calculator site:
  - index.html            national live calculator + a clickable 50-state map + a curated 15-state list
  - {state}.html           per-state hub: live calculator preset to that state + links to its salary presets
  - {state}-{N}k-paycheck-calculator.html   static preset detail page for one state+salary combo

Programmatic-SEO scope: all 50 states x 14 salary points ($20k-$150k, $10k steps) = 700 detail pages,
matching real search patterns (round salary numbers) rather than dense presets. The homepage's
"Browse by state" list stays limited to the original curated 15 (by population rank) to avoid a
cluttered 50-item list - the state map is the way to reach the rest.
"""
import json
import os

from calc import calculate, income_percentile, household_income_comparison
from state_data import STATES, STATE_ORDER, ALL_STATE_ORDER, MAP_STATES, PRETAX_NONCONFORMITY
from state_detail import STATE_DETAIL, NO_INCOME_TAX_TRADEOFF
import guides
from percentile_data import NATIONAL_INCOME_PERCENTILES, STATE_MEDIAN_HOUSEHOLD_INCOME
import federal_data
from static_pages import (
    about_html, privacy_html, money_icon,
    SITE_NAME, GA_SNIPPET, FOOTER_NAV, SITE_STYLE, SITE_HEADER, FAVICON,
)

OUTPUT_DIR = "docs"
BASE_URL = "https://uspaycheckcalc.github.io"

# Round-number anchors only. The earlier build generated a page for every $10k step from $20k to
# $150k - 700 near-identical pages whose text differed only in the numbers. Three anchors per state
# covers the salary figures people actually search for while leaving each page a reason to exist.
SALARIES = [50_000, 75_000, 100_000]


def fmt(n):
    return f"{n:,.0f}"


def marginal_rate(taxable, brackets):
    """The rate the next dollar of taxable income would be charged at."""
    if not brackets or taxable <= 0:
        return 0
    rate = brackets[0][1]
    for start, r in brackets:
        if taxable > start:
            rate = r
        else:
            break
    return rate


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
const PRETAX_NONCONFORMITY = {json.dumps(PRETAX_NONCONFORMITY)};
const NATIONAL_PERCENTILES = {json.dumps(NATIONAL_INCOME_PERCENTILES)};
const STATE_MEDIAN_HOUSEHOLD = {json.dumps(STATE_MEDIAN_HOUSEHOLD_INCOME)};

function incomePercentile(gross) {{
  const points = [[0, 0]].concat(NATIONAL_PERCENTILES);
  if (gross <= 0) return 0;
  if (gross >= points[points.length - 1][1]) return 99;
  for (let i = 0; i < points.length - 1; i++) {{
    const [p0, v0] = points[i], [p1, v1] = points[i + 1];
    if (gross >= v0 && gross <= v1) {{
      const frac = v1 !== v0 ? (gross - v0) / (v1 - v0) : 0;
      return p0 + frac * (p1 - p0);
    }}
  }}
  return 99;
}}

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

function calculatePaycheck(gross, stateKey, pretax401k, pretaxHsa) {{
  pretax401k = pretax401k || 0;
  pretaxHsa = pretaxHsa || 0;

  // 401(k) deferrals escape income tax but NOT FICA; HSA contributions through payroll escape both.
  const fedWages = Math.max(gross - pretax401k - pretaxHsa, 0);
  const fedTax = bracketTax(Math.max(fedWages - FEDERAL_STD_DEDUCTION, 0), FEDERAL_BRACKETS);

  const ficaWages = Math.max(gross - pretaxHsa, 0);
  const ss = Math.min(ficaWages, SS_WAGE_BASE) * SS_RATE;
  let medicare = ficaWages * MEDICARE_RATE;
  if (ficaWages > ADDL_MEDICARE_THRESHOLD) medicare += (ficaWages - ADDL_MEDICARE_THRESHOLD) * ADDL_MEDICARE_RATE;

  // A few states decline to follow the federal pre-tax treatment (PA taxes 401(k) deferrals; CA and
  // NJ tax HSA contributions), so the state exclusion is not always the same as the federal one.
  const nonconf = PRETAX_NONCONFORMITY[stateKey] || {{}};
  let excluded = 0;
  if (!nonconf.taxes_401k) excluded += pretax401k;
  if (!nonconf.taxes_hsa) excluded += pretaxHsa;
  const state = STATES[stateKey];
  const stateWages = Math.max(gross - excluded, 0);
  const stateTax = bracketTax(Math.max(stateWages - state.deduction, 0), state.brackets);

  const totalTax = fedTax + ss + medicare + stateTax;
  const pretaxTotal = pretax401k + pretaxHsa;
  // Money routed to a 401(k)/HSA is still yours, but it does not land in your bank account, so it is
  // not counted as take-home.
  const netAnnual = gross - totalTax - pretaxTotal;
  return {{ fedTax, ss, medicare, stateTax, totalTax, pretaxTotal, netAnnual, netMonthly: netAnnual / 12 }};
}}

function fmtUSD(n) {{ return '$' + Math.round(n).toLocaleString('en-US'); }}

function onSalaryInput(defaultState) {{
  const el = document.getElementById('salary');
  const cursorFromEnd = el.value.length - el.selectionStart;
  const digits = el.value.replace(/[^0-9]/g, '');
  el.value = digits === '' ? '' : parseInt(digits, 10).toLocaleString('en-US');
  const pos = Math.max(el.value.length - cursorFromEnd, 0);
  el.setSelectionRange(pos, pos);
  calc(defaultState);
}}

function calc(defaultState) {{
  const salaryEl = document.getElementById('salary');
  const stateEl = document.getElementById('state');
  const salary = parseFloat((salaryEl.value || '').replace(/,/g, '')) || 0;
  const stateKey = stateEl ? stateEl.value : defaultState;
  if (salary <= 0) return;
  const num = (id) => {{
    const el = document.getElementById(id);
    return el ? (parseFloat((el.value || '').replace(/,/g, '')) || 0) : 0;
  }};
  const r = calculatePaycheck(salary, stateKey, num('p401k'), num('phsa'));
  document.getElementById('r-federal').textContent = fmtUSD(r.fedTax);
  document.getElementById('r-state').textContent = fmtUSD(r.stateTax);
  document.getElementById('r-ss').textContent = fmtUSD(r.ss);
  document.getElementById('r-medicare').textContent = fmtUSD(r.medicare);
  document.getElementById('r-net-annual').textContent = fmtUSD(r.netAnnual);
  document.getElementById('r-net-monthly').textContent = fmtUSD(r.netMonthly);

  const pretaxRow = document.getElementById('row-pretax');
  if (pretaxRow) {{
    pretaxRow.style.display = r.pretaxTotal > 0 ? '' : 'none';
    document.getElementById('r-pretax').textContent = fmtUSD(r.pretaxTotal);
  }}
  const effEl = document.getElementById('r-effective');
  if (effEl) {{
    effEl.textContent = (r.totalTax / salary * 100).toFixed(1) + '% of gross pay goes to tax'
      + (r.pretaxTotal > 0 ? ', before your ' + fmtUSD(r.pretaxTotal) + ' of pre-tax contributions' : '');
  }}

  const pct = incomePercentile(salary);
  document.getElementById('r-percentile').textContent =
    (salary >= NATIONAL_PERCENTILES[NATIONAL_PERCENTILES.length - 1][1] ? 'Top 1%' : 'Top ' + Math.round(100 - pct) + '%')
    + ' of individual earners nationwide';

  const median = STATE_MEDIAN_HOUSEHOLD[stateKey];
  const diffPct = ((salary - median) / median) * 100;
  const state = STATES[stateKey];
  document.getElementById('r-household').textContent =
    fmtUSD(salary) + ' is ' + Math.abs(Math.round(diffPct)) + '% ' + (diffPct >= 0 ? 'above' : 'below')
    + ' the ' + state.name + ' median household income (' + fmtUSD(median) + ')';
}}
"""


CALC_JS = build_calc_js()


def calculator_box_html(default_state_key, fixed_state=False):
    if fixed_state:
        state_field = f'<input type="hidden" id="state" value="{default_state_key}">'
    else:
        options = "\n".join(
            f'<option value="{key}"{" selected" if key == default_state_key else ""}>{STATES[key]["name"]}</option>'
            for key in ALL_STATE_ORDER
        )
        state_field = f"""<div class="field">
      <label for="state">State</label>
      <select id="state" onchange="calc('{default_state_key}')">{options}</select>
    </div>"""

    return f"""<div class="calc-box">
    {state_field}
    <div class="field">
      <label for="salary">Annual salary (gross, $)</label>
      <input type="text" inputmode="numeric" id="salary" placeholder="e.g. 75,000" oninput="onSalaryInput('{default_state_key}')">
    </div>
    <details class="pretax">
      <summary>Add pre-tax contributions (401(k), HSA)</summary>
      <div class="field">
        <label for="p401k">Annual 401(k) contribution ($)</label>
        <input type="text" inputmode="numeric" id="p401k" placeholder="0" oninput="calc('{default_state_key}')">
      </div>
      <div class="field">
        <label for="phsa">Annual HSA contribution via payroll ($)</label>
        <input type="text" inputmode="numeric" id="phsa" placeholder="0" oninput="calc('{default_state_key}')">
      </div>
      <p class="source">401(k) deferrals reduce income tax but not Social Security or Medicare. HSA
      contributions made through payroll reduce both. See the
      <a href="pretax-401k-hsa-savings.html">guide to pre-tax contributions</a>.</p>
    </details>
    <div class="result">
      <div class="result-row"><span>Federal income tax</span><span id="r-federal">-</span></div>
      <div class="result-row"><span>State income tax</span><span id="r-state">-</span></div>
      <div class="result-row"><span>Social Security</span><span id="r-ss">-</span></div>
      <div class="result-row"><span>Medicare</span><span id="r-medicare">-</span></div>
      <div class="result-row" id="row-pretax" style="display:none"><span>Pre-tax contributions</span><span id="r-pretax">-</span></div>
      <div class="result-row total"><span>Net pay (annual)</span><span id="r-net-annual">-</span></div>
      <div class="result-row"><span>Net pay (monthly)</span><span id="r-net-monthly">-</span></div>
    </div>
    <div class="result compare">
      <div class="compare-row" id="r-effective">-</div>
      <div class="compare-row" id="r-percentile">-</div>
      <div class="compare-row" id="r-household">-</div>
    </div>
  </div>"""


MAP_TILE = 40
MAP_GAP = 4
MAP_PITCH = MAP_TILE + MAP_GAP
# Deep fills with light labels: the earlier pastel tiles were designed for a white page and turn
# into glowing blocks on the dark theme.
MAP_COLORS = {"none": "#14532d", "flat": "#1e3a8a", "progressive": "#4c1d95"}
MAP_TEXT_COLORS = {"none": "#86efac", "flat": "#93c5fd", "progressive": "#c4b5fd"}
MAP_LEGEND_LABELS = {"none": "No state income tax", "flat": "Flat tax rate", "progressive": "Progressive (bracketed) tax"}


def us_map_svg():
    tiles = []
    for key, m in MAP_STATES.items():
        state = STATES[key]
        x, y = m["col"] * MAP_PITCH, m["row"] * MAP_PITCH
        fill = MAP_COLORS[state["type"]]
        text_fill = MAP_TEXT_COLORS[state["type"]]
        tiles.append(
            f'<a href="{state_slug(key)}"><g><title>{state["name"]}: {MAP_LEGEND_LABELS[state["type"]]}</title>'
            f'<rect x="{x}" y="{y}" width="{MAP_TILE}" height="{MAP_TILE}" rx="6" fill="{fill}"></rect>'
            f'<text x="{x + MAP_TILE / 2:.0f}" y="{y + MAP_TILE / 2 + 4:.0f}" text-anchor="middle" '
            f'font-size="11" font-weight="700" fill="{text_fill}">{m["abbr"]}</text></g></a>'
        )

    width = (max(m["col"] for m in MAP_STATES.values()) + 1) * MAP_PITCH - MAP_GAP
    height = (max(m["row"] for m in MAP_STATES.values()) + 1) * MAP_PITCH - MAP_GAP

    legend = "".join(
        f'<span><i class="map-swatch" style="background:{color}"></i> {MAP_LEGEND_LABELS[key]}</span>'
        for key, color in MAP_COLORS.items()
    )

    return f"""
  <div class="us-map-wrap">
    <svg viewBox="0 0 {width} {height}" class="us-map" xmlns="http://www.w3.org/2000/svg">
      {''.join(tiles)}
    </svg>
    <div class="map-legend">{legend}</div>
  </div>
"""


DISCLAIMER = """
  <div class="disclaimer">
    * Estimates assume a single filer taking the standard deduction, with no dependents, credits,
    or additional withholding, for the 2026 tax year. Local/city income taxes (e.g. New York City)
    and other state-specific credits are not included. Federal and state tax rates change over
    time - see the About page for details and check a recent pay stub or a tax professional for
    exact figures.<br>
    * The national earner percentile is estimated from Census/CPS ASEC individual income data
    and linear interpolation between published percentile points - it is an approximation, not
    an exact rank. The state comparison uses median <b>household</b> income (Census ACS), a
    different population than an individual salary, shown for context only.
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
  <img class="hero-photo" src="images/hero-dollar-bills.jpg" alt="Close-up of US dollar bills" width="900" height="200" loading="eager">
  <h1>US Paycheck Calculator</h1>
  <p>Estimate your take-home pay after federal tax, Social Security, Medicare, and state income tax.
  Pick a state and enter your gross annual salary below.</p>

  {calculator_box_html("california")}

  <h2>Popular states</h2>
  <ul class="division-list">
  {state_links}
  </ul>

  <h2>All 50 states</h2>
  <p>Click any state for its paycheck calculator and common salary breakdowns.</p>
  {us_map_svg()}

  <div class="explain">
    <h2>What's included</h2>
    <p>This calculator covers all 50 states, including the nine states with no wage income tax
    (Texas, Florida, Washington, and others) alongside flat-tax and progressive-tax states. Each
    state's page carries that state's actual bracket schedule, its local income taxes, the payroll
    deductions that do not show up in a tax table, and any reciprocal agreements with neighbouring
    states.</p>
    <p>You can also add 401(k) and HSA contributions above. Those are handled properly rather than
    lumped together: a 401(k) deferral reduces income tax but not Social Security or Medicare, an
    HSA contribution through payroll reduces both, and Pennsylvania, California and New Jersey each
    decline to follow the federal treatment in their own way.</p>
  </div>

  <div class="explain">
    <h2>Why your real paycheck differs</h2>
    <p>A take-home figure is only as good as its assumptions, and this one assumes a single filer
    taking the standard deduction. If your pay stub disagrees, the reason is usually one of a short
    list of things - a W-4 that no longer matches your situation, a bonus withheld at the flat
    supplemental rate, a second job that each employer is taxing as though it were your only one, or
    a local tax that no state-level calculator can see.</p>
    <p><a href="guides.html">The guides</a> cover each of those in turn.</p>
  </div>
{DISCLAIMER}
"""
    return page_shell(
        f"{SITE_NAME} - Estimate Your Take-Home Pay by State",
        "Free US paycheck calculator: estimate take-home pay after federal tax, FICA, and state income tax for all 50 states.",
        body,
        extra_head='<meta name="naver-site-verification" content="38045222708a3b17b60bc932bd8fd8b63be1b2e4" />',
    )


def bracket_table_html(state_key):
    """Render the state's actual bracket schedule - the one piece of state tax data that is genuinely
    unique per state and that no amount of template text can substitute for."""
    state = STATES[state_key]
    if not state["brackets"]:
        return ""
    rows = []
    brackets = state["brackets"]
    for i, (start, rate) in enumerate(brackets):
        upper = brackets[i + 1][0] if i + 1 < len(brackets) else None
        if upper is None:
            band = f"${fmt(start)} and above" if start else "All taxable income"
        elif start == 0:
            band = f"$0 &ndash; ${fmt(upper)}"
        else:
            band = f"${fmt(start)} &ndash; ${fmt(upper)}"
        rows.append(f"<tr><td>{band}</td><td>{rate * 100:g}%</td></tr>")
    body = "\n".join(rows)
    name = state["name"]
    if state["deduction"]:
        ded = (f"<p>These bands apply to income after {name}'s ${fmt(state['deduction'])} standard "
               f"deduction or personal exemption, not to gross pay.</p>")
    else:
        ded = (f"<p>{name} gives wage earners no standard deduction or personal exemption, so these "
               f"rates apply from the first dollar of taxable wages.</p>")
    return f"""
  <h2>{state['name']} income tax rates for {federal_data.TAX_YEAR}</h2>
  <table>
    <tr><th>Taxable income</th><th>Marginal rate</th></tr>
    {body}
  </table>
  {ded}
"""


def no_income_tax_html(state_key):
    """Shown only for the nine states with no wage income tax, where the bracket table would be empty
    and the interesting question is what the state charges instead."""
    tradeoff = NO_INCOME_TAX_TRADEOFF.get(state_key)
    if not tradeoff:
        return ""
    state = STATES[state_key]
    return f"""
  <h2>What "no income tax" actually means in {state['name']}</h2>
  <p>{tradeoff}</p>
  <p>On the paycheck itself the effect is straightforward: the state income tax line is zero, so your
  take-home pay is your gross pay minus federal income tax and FICA. Compared with a state charging
  5% on the same salary, that is real money every month - the question is only whether the state
  takes it back somewhere outside the paycheck.</p>
"""


def local_tax_html(state_key):
    detail = STATE_DETAIL[state_key]
    if not detail["local_tax"]:
        return ""
    return f"""
  <div class="explain callout">
    <h2>Local income tax</h2>
    <p>{detail['local_tax']}</p>
    <p class="source">The estimate above covers federal and state tax only. Where a local tax
    applies, your actual take-home pay will be lower than shown.</p>
  </div>
"""


def reciprocity_html(state_key):
    state = STATES[state_key]
    partners = STATE_DETAIL[state_key]["reciprocity"]
    if not partners:
        return ""
    if len(partners) == 1:
        listed = partners[0]
    else:
        listed = ", ".join(partners[:-1]) + f" and {partners[-1]}"
    return f"""
  <h2>If you live in another state and work in {state['name']}</h2>
  <p>{state['name']} has reciprocal tax agreements with {listed}. If you live in one of those states
  and work in {state['name']}, your wages are taxed only by your home state - but you have to file an
  exemption certificate with your employer to make that happen. Without it, {state['name']} tax is
  withheld all year and you have to file a nonresident return to get it back.</p>
  <p><a href="working-across-state-lines.html">How working across state lines is taxed &rarr;</a></p>
"""


def payroll_html(state_key):
    state = STATES[state_key]
    items = STATE_DETAIL[state_key]["payroll"]
    if not items:
        return ""
    rows = "\n".join(f"<li><b>{name}</b> &mdash; {desc}</li>" for name, desc in items)
    return f"""
  <h2>Other {state['name']} payroll deductions</h2>
  <p>Beyond income tax and FICA, {state['name']} takes the following from employee paychecks. None of
  it is included in the estimate above, so a real pay stub will show a slightly smaller net figure:</p>
  <ul class="payroll-list">
  {rows}
  </ul>
"""


def filing_html(state_key):
    state = STATES[state_key]
    detail = STATE_DETAIL[state_key]
    agency, url = detail["revenue"]
    if detail["deadline"] is None:
        return f"""
  <h2>Filing in {state['name']}</h2>
  <p>{state['name']} does not tax wage income, so there is no state return to file on a salary. You
  still file a federal return, and you may still owe tax to another state if you earned income there.
  The <a href="{url}" rel="noopener">{agency}</a> administers the state's other taxes.</p>
"""
    return f"""
  <h2>Filing in {state['name']}</h2>
  <p>{state['name']} personal income tax returns are generally due <b>{detail['deadline']}</b>, and
  the return is administered by the <a href="{url}" rel="noopener">{agency}</a>. That is also where
  the authoritative bracket tables, nonresident and part-year forms, and withholding guidance live -
  this site estimates, the department decides.</p>
"""


def pretax_note_html(state_key):
    """Only shown for the states that break from the federal pre-tax treatment."""
    nonconf = PRETAX_NONCONFORMITY.get(state_key)
    if not nonconf:
        return ""
    state = STATES[state_key]
    if nonconf.get("taxes_401k"):
        what = (f"{state['name']} taxes 401(k) contributions as state income in the year you make them. "
                f"The federal deduction works as normal; the state one does not, so a 401(k) saves you "
                f"less here than in most states.")
    else:
        what = (f"{state['name']} does not follow the federal HSA rules. HSA contributions still reduce "
                f"your federal income tax and your Social Security and Medicare, but they remain subject "
                f"to {state['name']} income tax.")
    return f"""
  <div class="explain callout">
    <h2>Pre-tax contributions work differently here</h2>
    <p>{what}</p>
    <p class="source">The calculator above accounts for this. See the
    <a href="pretax-401k-hsa-savings.html">guide to pre-tax contributions</a> for the full comparison.</p>
  </div>
"""


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
  <div class="hero-icon small">{money_icon(44)}</div>
  <h1>{state['name']} Paycheck Calculator</h1>
  <p>{tax_type_desc} Enter your gross annual salary to estimate your {state['name']} take-home pay
  after federal income tax, Social Security, Medicare and state tax.</p>

  {calculator_box_html(state_key, fixed_state=True)}
  {note_html}

  {bracket_table_html(state_key)}
  {no_income_tax_html(state_key)}
  {local_tax_html(state_key)}
  {pretax_note_html(state_key)}
  {payroll_html(state_key)}
  {reciprocity_html(state_key)}
  {filing_html(state_key)}

  <h2>Common salaries in {state['name']}</h2>
  <ul class="division-list">
  {salary_links}
  </ul>

  <div class="nav"><a href="index.html">&larr; All states</a> | <a href="guides.html">Paycheck guides</a></div>
{DISCLAIMER}
"""
    return page_shell(
        f"{state['name']} Paycheck Calculator - Take-Home Pay by Salary ({federal_data.TAX_YEAR})",
        f"Estimate {state['name']} take-home pay after federal tax, FICA and state income tax, with "
        f"{state['name']}'s tax brackets, local income taxes and payroll deductions explained.",
        body,
    )


def detail_html(state_key, salary, prev_salary, next_salary):
    state = STATES[state_key]
    r = calculate(salary, state_key)
    effective_rate = r["total_tax"] / salary * 100
    fed_marginal = marginal_rate(salary - federal_data.STANDARD_DEDUCTION, federal_data.BRACKETS) * 100
    st_marginal = (marginal_rate(salary - state["deduction"], state["brackets"]) * 100
                   if state["brackets"] else 0)
    state_marginal_text = (f", and the {state['name']} marginal rate is {st_marginal:g}%"
                           if st_marginal else f", and {state['name']} adds nothing on top")
    pct = income_percentile(salary)
    pct_label = "Top 1%" if salary >= NATIONAL_INCOME_PERCENTILES[-1][1] else f"Top {round(100 - pct)}%"
    hh_median, hh_diff = household_income_comparison(salary, state_key)
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
    <h2>What ${salary:,} looks like per paycheck</h2>
    <p>Same annual pay, cut a different number of ways. Biweekly and semi-monthly are not the same
    thing: biweekly pays every two weeks and produces 26 checks a year, semi-monthly pays on fixed
    dates and produces 24 larger ones.</p>
    <table>
      <tr><th>Pay schedule</th><th>Gross per check</th><th>Take-home per check</th></tr>
      <tr><td>Weekly (52)</td><td>${fmt(salary / 52)}</td><td>${fmt(r['net_annual'] / 52)}</td></tr>
      <tr><td>Biweekly (26)</td><td>${fmt(salary / 26)}</td><td>${fmt(r['net_biweekly'])}</td></tr>
      <tr><td>Semi-monthly (24)</td><td>${fmt(salary / 24)}</td><td>${fmt(r['net_annual'] / 24)}</td></tr>
      <tr><td>Monthly (12)</td><td>${fmt(salary / 12)}</td><td>${fmt(r['net_monthly'])}</td></tr>
    </table>
  </div>

  <div class="explain">
    <h2>Effective vs. marginal rate</h2>
    <p>On ${salary:,} in {state['name']}, <b>{effective_rate:.1f}%</b> of gross pay goes to federal
    tax, state tax and FICA combined. That is the effective rate - the share of the whole salary.</p>
    <p>The marginal rate is a different number: it is what the <em>next</em> dollar is taxed at. On
    this salary the federal marginal bracket is <b>{fed_marginal:g}%</b>{state_marginal_text}. People
    conflate the two and conclude a raise will be mostly taxed away; the effective rate is what
    actually determines take-home pay, and it rises far more slowly than the bracket does.</p>
  </div>

  <div class="explain">
    <h2>How does ${salary:,} compare?</h2>
    <div class="compare-row">{pct_label} of individual earners nationwide (${salary:,} vs. the national distribution of earnings).</div>
    <div class="compare-row">${fmt(salary)} is {abs(round(hh_diff))}% {"above" if hh_diff >= 0 else "below"} the {state['name']} median <b>household</b> income (${fmt(hh_median)}) - note this compares an individual salary to a household total, not a like-for-like percentile.</div>
  </div>

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

  <div class="nav"><a href="{state_slug(state_key)}">&larr; More {state['name']} salaries</a> | <a href="index.html">All states</a> | <a href="guides.html">Paycheck guides</a></div>
{DISCLAIMER}
"""
    return page_shell(title, desc, body)


def guides_index_html():
    cards = []
    for g in guides.GUIDES:
        cards.append(
            f'<li><a href="{guides.guide_slug(g["slug"])}"><b>{g["title"]}</b></a>'
            f'<span class="guide-desc">{g["description"]}</span></li>'
        )
    cards_html = "\n".join(cards)
    body = f"""
  <h1>Paycheck Guides</h1>
  <p>The calculator tells you what your take-home pay is. These explain why it is that number, and
  what to do when it looks wrong.</p>
  <ul class="guide-list">
  {cards_html}
  </ul>
  <div class="nav"><a href="index.html">&larr; Back to the calculator</a></div>
"""
    return page_shell(
        f"Paycheck Guides - {SITE_NAME}",
        "Plain-English guides to US paycheck withholding: the W-4, pre-tax 401(k) and HSA "
        "contributions, bonus withholding, overtime, FICA, and working across state lines.",
        body,
    )


def guide_page_html(guide):
    return page_shell(
        f"{guide['title']} - {SITE_NAME}",
        guide["description"],
        guide["body"] + DISCLAIMER,
    )


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    valid_filenames = {"index.html", "about.html", "privacy.html", "guides.html",
                       "sitemap.xml", "ads.txt", "robots.txt"}
    for g in guides.GUIDES:
        valid_filenames.add(guides.guide_slug(g["slug"]))
    for key in ALL_STATE_ORDER:
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

    for key in ALL_STATE_ORDER:
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

    with open(os.path.join(OUTPUT_DIR, "guides.html"), "w", encoding="utf-8") as f:
        f.write(guides_index_html())
    urls.append(f"{BASE_URL}/guides.html")

    for g in guides.GUIDES:
        fname = guides.guide_slug(g["slug"])
        with open(os.path.join(OUTPUT_DIR, fname), "w", encoding="utf-8") as f:
            f.write(guide_page_html(g))
        urls.append(f"{BASE_URL}/{fname}")

    static_files = {"about.html": about_html(), "privacy.html": privacy_html()}
    for filename, html in static_files.items():
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(html)
        urls.append(f"{BASE_URL}/{filename}")

    print(f"Generated {len(urls)} pages -> {OUTPUT_DIR}/")
    return urls


if __name__ == "__main__":
    main()
