"""
Written guides for the site.

These exist for a different reason than the generated state/salary pages. Those answer "what is the
number"; these answer "why is the number what it is" - the questions a take-home figure provokes but
cannot itself address. They are hand-written, one topic each, and they are the part of the site that
is not derivable from a tax table.

Editorial rule, same as state_detail.py: any figure that the IRS re-sets every year (contribution
limits, exact bracket edges) is either pulled from federal_data so it stays in sync with the
calculator, or described rather than quoted. Statutory rules that do not drift - the 1.5x overtime
multiplier, the 22% supplemental rate, the FICA split - are stated directly.

Each guide is a dict: slug, title, description (meta), body (HTML fragment).
"""
import federal_data


def _fmt(n):
    return f"{n:,.0f}"


SS_RATE_PCT = federal_data.SOCIAL_SECURITY_RATE * 100
MEDICARE_RATE_PCT = federal_data.MEDICARE_RATE * 100
ADDL_MEDICARE_PCT = federal_data.ADDITIONAL_MEDICARE_RATE * 100
WAGE_BASE = _fmt(federal_data.SOCIAL_SECURITY_WAGE_BASE)
STD_DEDUCTION = _fmt(federal_data.STANDARD_DEDUCTION)
ADDL_MEDICARE_THRESHOLD = _fmt(federal_data.ADDITIONAL_MEDICARE_THRESHOLD_SINGLE)
TAX_YEAR = federal_data.TAX_YEAR

IRS_W4 = "https://www.irs.gov/forms-pubs/about-form-w-4"
IRS_ESTIMATOR = "https://www.irs.gov/individuals/tax-withholding-estimator"
IRS_PUB15 = "https://www.irs.gov/publications/p15"
IRS_RETIREMENT_LIMITS = "https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-topics-401k-and-profit-sharing-plan-contribution-limits"
IRS_HSA = "https://www.irs.gov/publications/p969"
SSA_WAGE_BASE = "https://www.ssa.gov/oact/cola/cbb.html"
DOL_OVERTIME = "https://www.dol.gov/agencies/whd/overtime"


GUIDES = [
    {
        "slug": "how-w4-withholding-works",
        "title": "How W-4 Withholding Actually Works (And Why a Big Refund Isn't a Win)",
        "description": "What the W-4 does, why your refund is not a bonus, and how to tell whether your withholding is set correctly.",
        "body": f"""
  <h1>How W-4 Withholding Actually Works</h1>
  <p class="lede">Your employer does not know what you will owe in tax. It makes an estimate, every
  payday, based on a form you filled out - possibly years ago, possibly in a hurry on your first
  day. Almost everything people find confusing about their paycheck starts there.</p>

  <h2>Withholding is a running guess, not a bill</h2>
  <p>Income tax in the United States is pay-as-you-go. You do not wait until April and settle up;
  money is taken out of each paycheck and sent to the IRS on your behalf throughout the year. The
  amount taken out is <em>withholding</em>, and it is calculated by your employer's payroll system
  from the Form W-4 you submitted.</p>
  <p>That calculation is a projection. Payroll takes the gross pay for this one period, annualises
  it as though every period this year will look the same, works out what the tax on that annual
  figure would be, and withholds one period's share. It is a reasonable guess, and it is wrong
  whenever your year does not actually look like that period - which is why mid-year raises,
  bonuses, unpaid leave, and second jobs all throw it off.</p>
  <p>At the end of the year, your actual liability is computed on your return. If withholding
  overshot, you get the excess back. If it undershot, you pay the difference. The refund is not a
  reward and the balance due is not a penalty; both are just the size of the error in the guess.</p>

  <h2>The 2020 redesign removed "allowances"</h2>
  <p>If you remember claiming a number of allowances, that form no longer exists. The W-4 was
  redesigned and now asks for dollar amounts and circumstances instead of a count. It has five
  steps, and most people genuinely only need two of them:</p>
  <ul>
    <li><b>Step 1</b> - name, address, filing status. Required.</li>
    <li><b>Step 2</b> - multiple jobs, or a working spouse. Skipped more often than it should be.</li>
    <li><b>Step 3</b> - dependents, which reduces withholding by a credit amount.</li>
    <li><b>Step 4</b> - other income, extra deductions, and a box for additional withholding per
    period. The optional fine-tuning.</li>
    <li><b>Step 5</b> - signature. Required.</li>
  </ul>
  <p>Fill in Steps 1 and 5 and nothing else, and payroll withholds as though you are a single filer
  with one job taking the standard deduction. For a lot of people that is accurate. For anyone with
  a second job or a working spouse, it is substantially wrong.</p>

  <h2>Why two jobs breaks it</h2>
  <p>This is the single most common cause of an unexpected April bill. Each employer withholds as
  though its paycheck is your only income. Each therefore applies the lowest brackets and the full
  standard deduction to its own slice of your pay. Stack two such calculations and you have claimed
  the standard deduction twice and run through the bottom brackets twice, while the IRS will apply
  each exactly once to your combined income.</p>
  <p>At a ${STD_DEDUCTION} standard deduction, that gap alone is sizeable before you reach the
  bracket effect. Step 2 of the W-4 exists specifically to correct this, either through the
  checkbox (when two jobs pay roughly the same) or the worksheet.</p>

  <h2>The refund is your money, returned late</h2>
  <p>A large refund means you lent the federal government money for up to sixteen months at zero
  interest. People like the lump sum, and there is a real behavioural argument for forced saving -
  but it should be a decision, not an accident. The opposite error carries an actual cost: if you
  underpay by enough, the IRS can charge an underpayment penalty even though you settled in full
  by the deadline.</p>

  <h2>Checking whether yours is right</h2>
  <p>Take a recent pay stub and multiply the federal income tax withheld by the number of pay
  periods left in the year, then add what has already been withheld year to date. Compare that
  against an estimate of your actual liability - the <a href="index.html">calculator on this
  site</a> will get you close for a single filer taking the standard deduction. A gap of a few
  hundred dollars is normal and not worth acting on. A gap of several thousand is worth a new W-4.</p>
  <p>Two things worth knowing about submitting one: you can file a new W-4 at any time, as many
  times as you like, and the cleanest correction mid-year is usually Step 4(c), extra withholding
  per period, because it is a flat dollar amount you control directly rather than an input into a
  formula you cannot see.</p>
  <p>The IRS publishes a <a href="{IRS_ESTIMATOR}" rel="noopener">Tax Withholding Estimator</a>
  that handles the cases this site's calculator deliberately does not - dependents, credits,
  itemised deductions, multiple jobs - and the <a href="{IRS_W4}" rel="noopener">Form W-4
  instructions</a> cover the worksheet in full.</p>

  <div class="guide-nav"><a href="guides.html">&larr; All guides</a></div>
""",
    },
    {
        "slug": "pretax-401k-hsa-savings",
        "title": "What a 401(k) and an HSA Actually Save You Per Paycheck",
        "description": "How pre-tax payroll deductions reduce take-home pay by less than you contribute, and why the HSA saves more per dollar than the 401(k).",
        "body": f"""
  <h1>What a 401(k) and an HSA Actually Save You Per Paycheck</h1>
  <p class="lede">Contributing $200 a paycheck to a 401(k) does not reduce your take-home pay by
  $200. It reduces it by $200 minus the tax you would have paid on that money - and how much that
  is depends on which account you use, which is where most of the confusion lives.</p>

  <h2>The mechanism</h2>
  <p>A pre-tax payroll deduction comes out of your gross pay before tax is calculated. Payroll
  reduces your taxable wages by the contribution, then computes withholding on the smaller figure.
  The money still leaves your paycheck, but some of what leaves would have gone to the government
  anyway.</p>
  <p>So the real cost of a contribution is not the contribution. It is the contribution times
  (1 - your marginal rate). At a 22% federal marginal rate with no state income tax, $200 diverted
  to a 401(k) costs you about $156 in take-home. In a state with a 5% income tax that also allows
  the deduction, it costs about $146.</p>

  <h2>The 401(k) and the HSA are not taxed the same way</h2>
  <p>This is the part that surprises people. Both reduce income tax. Only one reduces payroll tax.</p>
  <table>
    <tr><th></th><th>Federal income tax</th><th>Social Security &amp; Medicare</th></tr>
    <tr><td>Traditional 401(k) deferral</td><td>Reduced</td><td><b>Not reduced</b></td></tr>
    <tr><td>HSA via payroll (cafeteria plan)</td><td>Reduced</td><td><b>Reduced</b></td></tr>
  </table>
  <p>Elective 401(k) deferrals are exempt from income tax but remain fully subject to FICA. You pay
  {SS_RATE_PCT:g}% Social Security and {MEDICARE_RATE_PCT:g}% Medicare on that money on the way in -
  and, for the 401(k), income tax on the way out in retirement.</p>
  <p>HSA contributions routed through your employer's cafeteria plan escape both. That is an extra
  {SS_RATE_PCT + MEDICARE_RATE_PCT:g}% saved per dollar relative to the 401(k), on top of the income
  tax saving. It is the only common payroll deduction that avoids income tax, payroll tax, and - if
  spent on qualified medical expenses - tax on the way out as well.</p>
  <p>One caveat on the FICA point: contributing to an HSA by writing a cheque to the custodian
  yourself gets you the income tax deduction on your return but <em>not</em> the FICA saving. The
  payroll route is strictly better, and it is the same money.</p>

  <h2>Three states disagree with the federal treatment</h2>
  <p>State conformity is not automatic, and a few states decline:</p>
  <ul>
    <li><b>Pennsylvania</b> taxes 401(k) elective deferrals as state income in the year you make
    them. The federal deduction works; the Pennsylvania one does not.</li>
    <li><b>California</b> and <b>New Jersey</b> do not conform to the federal HSA rules. HSA
    contributions remain subject to state income tax in both, though they still escape FICA.</li>
  </ul>
  <p>The calculator on the state pages of this site accounts for these three, which is why the
  numbers for Pennsylvania, California and New Jersey move differently from the rest when you enter
  a contribution.</p>

  <h2>The employer match</h2>
  <p>If your employer matches 401(k) contributions, the match is the highest-return part of the
  whole arrangement and it has nothing to do with tax. A 50% match on the first 6% of salary is a
  50% return on that money, immediately, before any market exposure. Nothing else in a normal
  compensation package pays that. Contributing less than the match threshold means declining part
  of your stated salary.</p>

  <h2>Limits</h2>
  <p>Both accounts have annual contribution limits that the IRS resets each year, with higher
  ceilings for people above a catch-up age and, for the HSA, different limits for individual and
  family coverage. Because these move annually, this page does not quote them - check the current
  figures for <a href="{IRS_RETIREMENT_LIMITS}" rel="noopener">401(k) plans</a> and
  <a href="{IRS_HSA}" rel="noopener">health savings accounts</a> directly.</p>
  <p>The HSA has a gate the 401(k) does not: you must be covered by a qualifying high-deductible
  health plan to contribute at all. If you are not, the comparison above is moot.</p>

  <h2>When pre-tax is the wrong choice</h2>
  <p>Pre-tax contributions are a bet that your marginal rate now is higher than your marginal rate
  when you withdraw. That bet is good for most mid-career earners and bad for someone early in a
  career with a steeply rising income, who may be better served by a Roth contribution - taxed now
  at a low rate, untaxed later at a high one. The arithmetic on this page describes what pre-tax
  does, not whether you should choose it.</p>

  <div class="guide-nav"><a href="guides.html">&larr; All guides</a></div>
""",
    },
    {
        "slug": "why-your-bonus-is-taxed-higher",
        "title": "Why Your Bonus Looked Like It Was Taxed at 40% (It Wasn't)",
        "description": "Supplemental wage withholding explained: the flat 22% federal rate, why FICA and state tax stack on top, and why you get the difference back.",
        "body": f"""
  <h1>Why Your Bonus Looked Like It Was Taxed at 40%</h1>
  <p class="lede">A $5,000 bonus arrives as $3,200 and the obvious conclusion is that bonuses are
  taxed punitively. They are not. Bonuses are taxed at exactly the same rates as the rest of your
  income - they are <em>withheld</em> differently, and the difference comes back.</p>

  <h2>Supplemental wages have their own withholding rule</h2>
  <p>The IRS classifies bonuses, commissions, severance, back pay, and payouts of accrued leave as
  <em>supplemental wages</em>. They do not fit the normal withholding machinery, which assumes every
  paycheck looks like every other one. A $5,000 bonus annualised as though you receive it twenty-six
  times a year would project an income you do not have.</p>
  <p>So employers are given two options. The common one is the <b>flat rate method</b>: withhold a
  flat 22% federal income tax on the supplemental payment, ignoring your W-4 entirely. The other is
  the <b>aggregate method</b>: add the bonus to the regular paycheck and withhold on the combined
  amount using your W-4, which usually withholds more because the combined figure annualises into
  higher brackets.</p>
  <p>One rule worth knowing if you ever receive a very large payout: supplemental wages above $1
  million in a calendar year are withheld at 37%, the top federal rate, and the employer has no
  choice in the matter.</p>

  <h2>Where the rest of the money went</h2>
  <p>The 22% is only the federal income tax piece. A bonus is ordinary wages, so everything else
  applies too:</p>
  <table>
    <tr><th>Withheld from a bonus</th><th>Rate</th></tr>
    <tr><td>Federal income tax (flat rate method)</td><td>22%</td></tr>
    <tr><td>Social Security</td><td>{SS_RATE_PCT:g}% (up to the ${WAGE_BASE} wage base)</td></tr>
    <tr><td>Medicare</td><td>{MEDICARE_RATE_PCT:g}%</td></tr>
    <tr><td>State income tax</td><td>Varies; many states have their own supplemental rate</td></tr>
  </table>
  <p>Stack those and a bonus in a mid-tax state loses roughly a third before anything unusual has
  happened. Add a 401(k) deferral that applies to bonuses - many plans do by default - and the
  deposit shrinks again, though that portion is not tax at all; it is your money, moved.</p>

  <h2>You get the difference back</h2>
  <p>Here is the part that matters. Withholding is not the tax. Your actual liability is computed on
  your return across all your income, with no distinction between salary and bonus - a dollar of
  bonus is taxed at the same marginal rate as a dollar of salary.</p>
  <p>If your true marginal rate is 12%, a bonus withheld at 22% was over-withheld, and the excess
  comes back as a larger refund. If your marginal rate is 32%, the flat 22% under-withheld and you
  will owe the difference. The bonus did not change your tax; it changed the timing of its payment.</p>
  <p>This is why the flat method can quietly cause an April bill for higher earners. If your income
  puts you above the 22% bracket and you receive a substantial bonus, consider adding extra
  withholding on Form W-4 for the remainder of the year rather than discovering the gap in April.</p>

  <h2>What you cannot do</h2>
  <p>You cannot ask your employer to use the aggregate method instead of the flat method, or the
  other way round; the choice belongs to the employer's payroll process. What you can influence is
  your regular withholding around the bonus, and whether your 401(k) election applies to supplemental
  pay - many plans let you set a separate bonus deferral percentage, which is the usual way people
  route an unexpected payment into retirement savings without touching their normal contribution.</p>

  <p class="source">The withholding rules for supplemental wages are set out in
  <a href="{IRS_PUB15}" rel="noopener">IRS Publication 15 (Circular E)</a>.</p>

  <div class="guide-nav"><a href="guides.html">&larr; All guides</a></div>
""",
    },
    {
        "slug": "hourly-vs-salary-take-home",
        "title": "Hourly vs. Salary: Converting Between Them Without Fooling Yourself",
        "description": "How to convert an hourly rate to an annual salary and back, why the 2,080-hour rule overstates some jobs, and what overtime eligibility is really worth.",
        "body": f"""
  <h1>Hourly vs. Salary: Converting Without Fooling Yourself</h1>
  <p class="lede">The standard conversion - hourly rate times 2,080 - is a decent first pass and a
  bad final answer. It assumes a year with no unpaid time, no overtime, and no variation in hours,
  which describes a salaried job rather than an hourly one.</p>

  <h2>Where 2,080 comes from</h2>
  <p>Forty hours a week times fifty-two weeks. $30 an hour becomes $62,400 a year; $75,000 a year
  becomes about $36.06 an hour. Use it for quick comparisons, because everyone else does.</p>
  <p>It is accurate for a salaried employee, who is paid the same whether a given week runs long or
  short. For an hourly employee it is an upper bound, and the gap can be large. Two weeks of unpaid
  leave takes the real figure to 2,000 hours. Unpaid holidays, slow seasons, and shifts that get cut
  take it lower. Comparing a salary offer against an hourly one at 2,080 flatters the hourly job
  unless the hours are genuinely guaranteed.</p>

  <h2>Overtime is the thing that moves the number</h2>
  <p>Under the Fair Labor Standards Act, non-exempt employees must be paid at least 1.5 times their
  regular rate for hours over 40 in a workweek. That is a federal floor; several states require
  more, most notably daily overtime after 8 hours in a day, and double time in some circumstances.</p>
  <p>The effect compounds quickly. At $30 an hour, five overtime hours a week pay $225 - roughly
  $11,700 a year, or an 18% increase over the 2,080-hour base. An hourly job with reliable overtime
  can out-earn a salaried job with a nominally higher headline figure.</p>
  <p>The reverse is the thing to watch in an offer. Moving from an hourly role to a salaried one
  usually means becoming exempt from overtime, and the extra hours stop being paid. A 10% raise that
  converts ten paid overtime hours a week into unpaid ones is a pay cut. Whether a salaried role is
  genuinely exempt depends on both a salary threshold and the actual duties of the job - the title
  alone does not decide it.</p>

  <h2>Pay frequency changes the paycheck, not the pay</h2>
  <p>Payroll calendars are a common source of false alarm:</p>
  <table>
    <tr><th>Schedule</th><th>Periods per year</th><th>On a $75,000 salary</th></tr>
    <tr><td>Weekly</td><td>52</td><td>$1,442 gross</td></tr>
    <tr><td>Biweekly</td><td>26</td><td>$2,885 gross</td></tr>
    <tr><td>Semi-monthly</td><td>24</td><td>$3,125 gross</td></tr>
    <tr><td>Monthly</td><td>12</td><td>$6,250 gross</td></tr>
  </table>
  <p>Biweekly and semi-monthly sound interchangeable and are not. Biweekly means every two weeks,
  which produces 26 paychecks and, twice a year, a month with three of them. Semi-monthly means
  twice a month on fixed dates, which produces 24 larger ones. Same annual pay, different cash flow,
  and the "extra" biweekly paycheck is not extra money - it is the same total cut into more pieces.</p>

  <h2>What the comparison usually misses</h2>
  <p>Hourly and salaried roles frequently differ in ways that do not appear in either number:
  employer health insurance contributions, 401(k) match, paid leave, and the predictability of the
  hours themselves. An employer paying a meaningful share of a family health premium is providing
  several thousand dollars of untaxed value that no hourly conversion captures.</p>
  <p>If you are comparing two concrete offers, convert both to an annual figure, then run each
  through the <a href="index.html">take-home calculator</a> for the state in question - the gap
  after tax is not always proportional to the gap before it, particularly across a state line.</p>

  <p class="source">Federal overtime rules, including the exemption tests, are published by the
  <a href="{DOL_OVERTIME}" rel="noopener">U.S. Department of Labor</a>. State rules can be stricter
  and override the federal floor.</p>

  <div class="guide-nav"><a href="guides.html">&larr; All guides</a></div>
""",
    },
    {
        "slug": "social-security-medicare-payroll-tax",
        "title": "FICA Explained: The Wage Base, the Surtax, and Why It Stops Mid-Year",
        "description": "How Social Security and Medicare are withheld, why high earners see their paycheck grow in autumn, and what the extra 0.9% Medicare tax is.",
        "body": f"""
  <h1>FICA Explained: Social Security, Medicare, and the Mid-Year Raise That Isn't</h1>
  <p class="lede">FICA is the most predictable tax on your paycheck and the one with the strangest
  shape. It is flat, it has a ceiling that applies to one half and not the other, and for some
  people it simply stops partway through the year.</p>

  <h2>Two taxes, not one</h2>
  <p>The line on your pay stub marked FICA - or split into two lines - is a pair of separate taxes
  with different rules:</p>
  <table>
    <tr><th>Tax</th><th>Employee rate</th><th>Applies to</th></tr>
    <tr><td>Social Security (OASDI)</td><td>{SS_RATE_PCT:g}%</td><td>Wages up to ${WAGE_BASE} for {TAX_YEAR}</td></tr>
    <tr><td>Medicare</td><td>{MEDICARE_RATE_PCT:g}%</td><td>Every dollar of wages, no ceiling</td></tr>
  </table>
  <p>Your employer pays the same amounts again on your behalf, which is why the combined figure is
  sometimes quoted as 15.3%. If you are self-employed you pay both halves yourself as
  self-employment tax, with a deduction for the employer half.</p>
  <p>Unlike income tax, there is nothing to configure. Your W-4 does not affect FICA. Filing status
  does not affect FICA. It is a flat percentage of wages, which is why it is the one number on this
  site's estimates least likely to be wrong for your situation.</p>

  <h2>The wage base, and the paycheck that suddenly grows</h2>
  <p>Social Security stops once your year-to-date wages pass the wage base - ${WAGE_BASE} for
  {TAX_YEAR}, reset upward most years for wage growth. Past that point, the {SS_RATE_PCT:g}%
  disappears from your paycheck for the rest of the calendar year, and in January it comes back.</p>
  <p>Earn well above the base and you will see your net pay jump one autumn payday with no
  explanation on the stub. Nothing has changed about your salary; you have simply finished paying
  that tax for the year. Medicare has no such ceiling and keeps going at {MEDICARE_RATE_PCT:g}%
  regardless.</p>
  <p>This is also the mechanism that makes Social Security regressive as a share of income. Someone
  earning the wage base pays {SS_RATE_PCT:g}% of their whole salary; someone earning twice that pays
  {SS_RATE_PCT / 2:g}%.</p>

  <h2>The Additional Medicare Tax</h2>
  <p>Above ${ADDL_MEDICARE_THRESHOLD} in wages for a single filer, an extra {ADDL_MEDICARE_PCT:g}%
  Medicare tax applies to the excess, taking the marginal Medicare rate to
  {MEDICARE_RATE_PCT + ADDL_MEDICARE_PCT:g}%. The employer does not match this one - it is
  employee-only.</p>
  <p>It has a quirk worth knowing if you are married. Employers are required to begin withholding it
  once <em>your individual</em> wages pass ${ADDL_MEDICARE_THRESHOLD}, but the threshold on the
  actual return is based on <em>combined</em> income and is lower for married couples filing jointly
  than twice the single figure. Two spouses each earning somewhat under the individual threshold can
  therefore owe the tax without a cent of it having been withheld, and discover it at filing.</p>

  <h2>Changing jobs can over-withhold it</h2>
  <p>The Social Security wage base is tracked per employer, not per person. Switch jobs mid-year and
  your new employer starts counting from zero, with no knowledge of what the previous one already
  withheld. If your combined wages exceed the wage base, you will have overpaid Social Security.</p>
  <p>This is recoverable - you claim the excess as a credit on your federal return - but nobody tells
  you it happened, so it is worth checking your W-2s against the wage base in any year you changed
  employers. The same does not apply to the employer's half, which is not refundable to you.</p>

  <h2>What FICA does not fund</h2>
  <p>A common misreading of a pay stub: the Social Security line is not a savings account with your
  name on it. Current contributions fund current beneficiaries, and your eventual benefit is
  calculated from your earnings history rather than from a balance. The practical consequence is
  that years of low or no earnings dilute the average that benefit is based on - which matters more
  than most people assume when weighing a long career break.</p>

  <p class="source">The Social Security wage base for each year is published by the
  <a href="{SSA_WAGE_BASE}" rel="noopener">Social Security Administration</a>.</p>

  <div class="guide-nav"><a href="guides.html">&larr; All guides</a></div>
""",
    },
    {
        "slug": "working-across-state-lines",
        "title": "Working in One State and Living in Another: Who Taxes You?",
        "description": "Reciprocal agreements, part-year residency, credits for taxes paid to another state, and the remote-work rule that catches people out.",
        "body": f"""
  <h1>Working in One State and Living in Another</h1>
  <p class="lede">The default rule is uncomfortable: a state can tax you because you live there, and
  another state can tax you because you earned the money there. Both claims are valid at once. What
  stops you being taxed twice is a patchwork of agreements and credits that you have to actually
  claim.</p>

  <h2>Two kinds of claim</h2>
  <p>States tax income on two different bases. <b>Residents</b> are taxed on everything they earn,
  wherever they earn it. <b>Nonresidents</b> are taxed on income sourced to that state - typically
  wages for work physically performed inside its borders.</p>
  <p>Live in New Jersey and commute to an office in New York and both claims apply to the same
  salary. The resolution is not that one state backs down; it is that your home state gives you a
  credit for the tax you paid to the other one. You file a nonresident return where you worked, a
  resident return where you live, and claim the credit on the resident return.</p>
  <p>The credit is usually limited to what your home state would have charged on that income. If the
  work state's rate is higher, the credit does not fully cover it and you end up paying the higher of
  the two rates overall. Crossing into a high-tax state for work costs you real money even with the
  credit working correctly.</p>

  <h2>Reciprocal agreements: the clean case</h2>
  <p>Some neighbouring states have signed agreements that remove the problem entirely. Under a
  reciprocal agreement, a nonresident who works in the state owes it nothing on those wages and is
  taxed only by their home state. No nonresident return, no credit calculation.</p>
  <p>These are concentrated in the Midwest and Mid-Atlantic, where state lines cut through
  metropolitan areas - Illinois with its neighbours, the Pennsylvania-New Jersey agreement, the
  Maryland-Virginia-West Virginia-DC cluster, and Ohio, Indiana, Kentucky and Michigan with each
  other. Each <a href="index.html">state page on this site</a> lists that state's reciprocal
  partners.</p>
  <p>Reciprocity is not automatic. You have to file an exemption certificate with your employer -
  a different form in each state - telling them to withhold for your home state instead. Miss it and
  the wrong state withholds all year, which is recoverable only by filing a nonresident return to
  claim it all back. The agreements also cover wages only; other income is unaffected.</p>

  <h2>Moving mid-year</h2>
  <p>Move and you are a part-year resident of two states. Each taxes the income you earned while
  living there, and you file a part-year return in both, splitting your income by date. Your W-2 may
  not split cleanly, so keep the date of the move and a pay stub from around it.</p>
  <p>If you are moving <em>to</em> a state with no income tax, the timing of a bonus or vested equity
  can matter a great deal, since it is generally taxed by the state you lived in when you received
  it - though states differ on sourcing equity compensation earned over a vesting period, and a
  large award is worth a professional opinion rather than a rule of thumb.</p>

  <h2>Remote work is where people get caught</h2>
  <p>Working from home in one state for an employer headquartered in another is usually
  straightforward: wages are sourced to where you physically do the work, so your home state taxes
  them and the employer's state does not.</p>
  <p>The exception is the <b>convenience of the employer</b> rule, applied by a handful of states
  including New York. Under it, days you work remotely are treated as days worked <em>in the
  employer's state</em> unless you work remotely because the employer requires it - rather than for
  your own convenience. A New York employer with a remote employee elsewhere can therefore leave that
  employee owing New York tax on days never spent in New York, with the home state's credit not
  necessarily covering it.</p>
  <p>Travelling for work raises a quieter version of the same issue: many states can tax wages for
  days physically worked there, sometimes from the first day, and the thresholds vary. For a few days
  a year nobody pursues it; for a consultant spending months on a client site it is a real filing
  obligation.</p>

  <h2>What to check</h2>
  <ul>
    <li>Does your work state have a reciprocal agreement with your home state? If so, file the
    exemption certificate with your employer now rather than sorting it out in April.</li>
    <li>Is your employer withholding for the right state? A payroll system set up before you moved
    will keep withholding for the old one indefinitely.</li>
    <li>If you work remotely for an out-of-state employer, does that state apply a convenience rule?</li>
    <li>If you changed states mid-year, do you have the date and the income split?</li>
  </ul>
  <p>The calculator on this site estimates a single state's tax at a time, which is the right tool
  for comparing two states but not for modelling a split year - for that, the nonresident and
  part-year forms published by each state's revenue department, linked from every state page here,
  are the authoritative source.</p>

  <div class="guide-nav"><a href="guides.html">&larr; All guides</a></div>
""",
    },
]

GUIDES_BY_SLUG = {g["slug"]: g for g in GUIDES}


def guide_slug(slug):
    return f"{slug}.html"
