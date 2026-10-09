"""
Per-state editorial detail for the state hub pages.

This is deliberately SEPARATE from state_data.py: that file holds the numbers the calculator does
arithmetic with, this one holds the things a reader needs to know but the calculator does not model.
Every field here answers a question the take-home number alone leaves open ("why is my real check
smaller than this?", "I live in one state and work in another", "where do I actually file?").

Data-quality rule for this file (see also the note at the top of state_data.py): where a rate changes
frequently or varies by locality, name the tax and point at the agency rather than hardcoding a
number that will silently go stale. Dollar/percent figures appear here only where they are set in
statute and stable. The state income tax brackets themselves live in state_data.py and are rendered
from there, so they are never duplicated.

Fields:
  local_tax    - None, or a sentence describing local/municipal income taxes on wages. These are NOT
                 included in the calculator's estimate, which is why they are called out per state.
  reciprocity  - list of state names with which this state has a wage-tax reciprocal agreement (a
                 nonresident who works here files only in their home state). Empty list = none.
  payroll      - list of (program name, what it is) for state payroll deductions taken from the
                 EMPLOYEE's check that are not income tax and are not in the estimate.
  revenue      - (agency name, url) - the state's own tax authority.
  deadline     - personal income tax filing deadline, or None for states with no wage income tax.
"""

NO_TAX_REVENUE_NOTE = (
    "This state does not tax wage income, so there is no state income tax return to file on a salary."
)

# For the nine states with no wage income tax, the useful question is not "what is the rate" - it is
# "what does the state charge instead". Every state has to raise revenue somehow, and the substitute
# is what makes a no-income-tax state a better or worse deal for a particular person. Kept
# qualitative on purpose: sales and property tax rates are set locally and move constantly, so naming
# the mechanism is durable where quoting a rate would not be.
NO_INCOME_TAX_TRADEOFF = {
    "alaska": "Alaska is the unusual case: it levies no state income tax and no state sales tax, "
              "funding itself largely from oil and gas revenue, and it pays residents an annual "
              "Permanent Fund Dividend rather than collecting from them. The offsetting costs are "
              "local - many boroughs levy their own sales and property taxes - and a cost of living "
              "that is among the highest in the country, particularly off the road system.",
    "florida": "Florida replaces income tax revenue largely with sales tax and with property tax "
               "collected at the county level, supported by a tourism base that lets the state export "
               "part of its tax burden to visitors. Property tax is the one to check before assuming a "
               "move here is a straight gain: the homestead exemption materially favours established "
               "primary residents over new arrivals and second-home buyers.",
    "nevada": "Nevada funds itself through sales tax and heavy gaming and tourism levies, which is how "
              "a state with a small population supports itself without taxing wages. Sales tax is "
              "comparatively high as a result, so the benefit is larger for a high earner who saves a "
              "lot of income than for a household that spends most of what it earns.",
    "new-hampshire": "New Hampshire taxes no wages and has no general sales tax, and closes the gap "
                     "with some of the highest property taxes in the country - levied locally, so the "
                     "rate depends heavily on the town. For a renter this is an unusually good deal; "
                     "for a homeowner it can erase the income tax saving entirely. Note that living "
                     "here and working in Massachusetts means paying Massachusetts income tax on those "
                     "wages, which catches out a lot of people on that border.",
    "south-dakota": "South Dakota relies on sales tax, which it applies to a broader range of goods "
                    "and services than many states do, along with local property tax. Its tax code is "
                    "also notably friendly to trusts and financial institutions, which brings in "
                    "revenue that has nothing to do with resident wages.",
    "tennessee": "Tennessee has no wage income tax and among the highest combined state and local "
                 "sales tax rates in the country, including on groceries at a reduced rate. The "
                 "structure is regressive by design: it favours high earners and savers and bears "
                 "harder on households that spend most of their income.",
    "texas": "Texas has no state income tax and raises the difference through sales tax and some of "
             "the highest effective property tax rates in the country, set and collected locally by "
             "counties, cities and school districts. For a renter the no-income-tax benefit is close "
             "to pure gain. For a homeowner, the annual property tax bill frequently offsets a large "
             "part of what an income tax would have cost - so comparing a Texas offer against one in "
             "an income-tax state means comparing property tax bills, not just paychecks.",
    "washington": "Washington taxes no wage income and leans on sales tax and the business and "
                  "occupation tax instead. Two things qualify the picture: the state has a capital "
                  "gains tax on large long-term gains, which matters for anyone with significant "
                  "equity compensation, and employees pay into Paid Family and Medical Leave and the "
                  "WA Cares long-term care fund through payroll - so a Washington pay stub is not "
                  "quite as clean as 'no state tax' implies.",
    "wyoming": "Wyoming levies no income tax and keeps other taxes low as well, funded substantially "
               "by severance taxes on mineral, oil and gas extraction. That makes it one of the "
               "genuinely low-total-tax states rather than one that shifts the burden elsewhere - with "
               "the trade-off being a small population, limited services, and a job market "
               "concentrated in a few industries.",
}

STATE_DETAIL = {
    "alabama": {
        "local_tax": "Several Alabama cities, including Birmingham, Gadsden and Macon County, levy an "
                     "occupational tax on wages earned inside the city. It is withheld by the employer and "
                     "is separate from the state income tax.",
        "reciprocity": [],
        "payroll": [],
        "revenue": ("Alabama Department of Revenue", "https://www.revenue.alabama.gov/"),
        "deadline": "April 15",
    },
    "alaska": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [
            ("Unemployment insurance (employee share)",
             "Alaska is one of very few states where employees, not just employers, pay into the "
             "state unemployment insurance fund through a payroll deduction."),
        ],
        "revenue": ("Alaska Department of Revenue", "https://tax.alaska.gov/"),
        "deadline": None,
    },
    "arizona": {
        "local_tax": None,
        "reciprocity": ["California", "Indiana", "Oregon", "Virginia"],
        "payroll": [],
        "revenue": ("Arizona Department of Revenue", "https://azdor.gov/"),
        "deadline": "April 15",
    },
    "arkansas": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("Arkansas Department of Finance and Administration", "https://www.dfa.arkansas.gov/income-tax/"),
        "deadline": "April 15",
    },
    "california": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [
            ("State Disability Insurance (SDI)",
             "A mandatory employee-paid payroll deduction that funds disability and Paid Family Leave "
             "benefits. California removed the taxable wage ceiling in 2024, so SDI now applies to the "
             "whole salary - which makes it a visible gap between this estimate and a real California "
             "pay stub, especially at higher incomes."),
        ],
        "revenue": ("California Franchise Tax Board", "https://www.ftb.ca.gov/"),
        "deadline": "April 15",
    },
    "colorado": {
        "local_tax": "A handful of Colorado cities - Denver, Aurora, Greenwood Village, Glendale and "
                     "Sheridan - charge an occupational privilege tax. It is a small flat dollar amount per "
                     "month rather than a percentage of pay.",
        "reciprocity": [],
        "payroll": [
            ("FAMLI (Paid Family and Medical Leave Insurance)",
             "Colorado's paid-leave program is funded by a payroll contribution split between employer "
             "and employee, deducted from each check."),
        ],
        "revenue": ("Colorado Department of Revenue", "https://tax.colorado.gov/"),
        "deadline": "April 15",
    },
    "connecticut": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [
            ("Paid Leave (CT Paid Leave)",
             "Connecticut's paid family and medical leave program is funded entirely by an employee "
             "payroll deduction."),
        ],
        "revenue": ("Connecticut Department of Revenue Services", "https://portal.ct.gov/DRS"),
        "deadline": "April 15",
    },
    "delaware": {
        "local_tax": "Wilmington levies a city wage tax on income earned within the city, withheld "
                     "alongside state tax.",
        "reciprocity": [],
        "payroll": [
            ("Paid Leave (Delaware Paid Leave)",
             "Delaware's paid family and medical leave program is funded by payroll contributions, part "
             "of which may be deducted from the employee's check."),
        ],
        "revenue": ("Delaware Division of Revenue", "https://revenue.delaware.gov/"),
        "deadline": "April 30",
    },
    "florida": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("Florida Department of Revenue", "https://floridarevenue.com/"),
        "deadline": None,
    },
    "georgia": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("Georgia Department of Revenue", "https://dor.georgia.gov/"),
        "deadline": "April 15",
    },
    "hawaii": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [
            ("Temporary Disability Insurance (TDI)",
             "Hawaii employers must provide TDI coverage and may deduct up to half the cost from the "
             "employee, subject to a statutory cap."),
        ],
        "revenue": ("Hawaii Department of Taxation", "https://tax.hawaii.gov/"),
        "deadline": "April 20",
    },
    "idaho": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("Idaho State Tax Commission", "https://tax.idaho.gov/"),
        "deadline": "April 15",
    },
    "illinois": {
        "local_tax": None,
        "reciprocity": ["Iowa", "Kentucky", "Michigan", "Wisconsin"],
        "payroll": [],
        "revenue": ("Illinois Department of Revenue", "https://tax.illinois.gov/"),
        "deadline": "April 15",
    },
    "indiana": {
        "local_tax": "Every Indiana county levies its own local income tax on top of the state rate, at a "
                     "rate set by the county. This is withheld based on the county you lived in on "
                     "January 1, and it is a real percentage of pay - not a token fee - so an Indiana "
                     "paycheck is noticeably smaller than a state-rate-only estimate suggests.",
        "reciprocity": ["Kentucky", "Michigan", "Ohio", "Pennsylvania", "Wisconsin"],
        "payroll": [],
        "revenue": ("Indiana Department of Revenue", "https://www.in.gov/dor/"),
        "deadline": "April 15",
    },
    "iowa": {
        "local_tax": "Many Iowa school districts add a surtax calculated as a percentage of your state "
                     "income tax liability, so it scales with the state tax rather than with gross pay.",
        "reciprocity": ["Illinois"],
        "payroll": [],
        "revenue": ("Iowa Department of Revenue", "https://revenue.iowa.gov/"),
        "deadline": "April 30",
    },
    "kansas": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("Kansas Department of Revenue", "https://www.ksrevenue.gov/"),
        "deadline": "April 15",
    },
    "kentucky": {
        "local_tax": "Most Kentucky counties and cities charge an occupational license fee on wages "
                     "earned there - Louisville and Lexington among them. It is withheld by the employer "
                     "and is in addition to the flat state rate.",
        "reciprocity": ["Illinois", "Indiana", "Michigan", "Ohio", "Virginia", "West Virginia", "Wisconsin"],
        "payroll": [],
        "revenue": ("Kentucky Department of Revenue", "https://revenue.ky.gov/"),
        "deadline": "April 15",
    },
    "louisiana": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("Louisiana Department of Revenue", "https://revenue.louisiana.gov/"),
        "deadline": "May 15",
    },
    "maine": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [
            ("Paid Family and Medical Leave",
             "Maine's paid-leave program is funded by payroll contributions shared between employer and "
             "employee."),
        ],
        "revenue": ("Maine Revenue Services", "https://www.maine.gov/revenue/"),
        "deadline": "April 15",
    },
    "maryland": {
        "local_tax": "Every Maryland county and Baltimore City levies a local income tax, charged as a "
                     "percentage of your Maryland taxable income and collected on the same return. This is "
                     "one of the largest local-tax gaps in the country - a Maryland estimate that uses only "
                     "the state rate understates the tax meaningfully, and the rate depends on the county "
                     "you live in, not the one you work in.",
        "reciprocity": ["Pennsylvania", "Virginia", "West Virginia"],
        "payroll": [],
        "revenue": ("Comptroller of Maryland", "https://www.marylandtaxes.gov/"),
        "deadline": "April 15",
    },
    "massachusetts": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [
            ("Paid Family and Medical Leave (PFML)",
             "Massachusetts PFML is funded by a payroll contribution, part of which is withheld from the "
             "employee's wages."),
        ],
        "revenue": ("Massachusetts Department of Revenue",
                    "https://www.mass.gov/orgs/massachusetts-department-of-revenue"),
        "deadline": "April 15",
    },
    "michigan": {
        "local_tax": "Two dozen Michigan cities levy their own income tax, Detroit among them, typically "
                     "at one rate for residents and a lower rate for nonresidents who work in the city.",
        "reciprocity": ["Illinois", "Indiana", "Kentucky", "Minnesota", "Ohio", "Wisconsin"],
        "payroll": [],
        "revenue": ("Michigan Department of Treasury", "https://www.michigan.gov/taxes"),
        "deadline": "April 15",
    },
    "minnesota": {
        "local_tax": None,
        "reciprocity": ["Michigan", "North Dakota"],
        "payroll": [
            ("Paid Leave",
             "Minnesota's state paid family and medical leave program is funded by payroll contributions "
             "shared between employer and employee."),
        ],
        "revenue": ("Minnesota Department of Revenue", "https://www.revenue.state.mn.us/"),
        "deadline": "April 15",
    },
    "mississippi": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("Mississippi Department of Revenue", "https://www.dor.ms.gov/"),
        "deadline": "April 15",
    },
    "missouri": {
        "local_tax": "Kansas City and St. Louis each levy a 1% earnings tax on wages earned in the city, "
                     "withheld by the employer and owed whether or not you live there.",
        "reciprocity": [],
        "payroll": [],
        "revenue": ("Missouri Department of Revenue", "https://dor.mo.gov/"),
        "deadline": "April 15",
    },
    "montana": {
        "local_tax": None,
        "reciprocity": ["North Dakota"],
        "payroll": [],
        "revenue": ("Montana Department of Revenue", "https://mtrevenue.gov/"),
        "deadline": "April 15",
    },
    "nebraska": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("Nebraska Department of Revenue", "https://revenue.nebraska.gov/"),
        "deadline": "April 15",
    },
    "nevada": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("Nevada Department of Taxation", "https://tax.nv.gov/"),
        "deadline": None,
    },
    "new-hampshire": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("New Hampshire Department of Revenue Administration", "https://www.revenue.nh.gov/"),
        "deadline": None,
    },
    "new-jersey": {
        "local_tax": None,
        "reciprocity": ["Pennsylvania"],
        "payroll": [
            ("Temporary Disability Insurance (TDI)",
             "An employee-paid payroll deduction funding short-term disability benefits."),
            ("Family Leave Insurance (FLI)",
             "A second employee-paid deduction funding New Jersey's paid family leave benefits."),
        ],
        "revenue": ("New Jersey Division of Taxation", "https://www.nj.gov/treasury/taxation/"),
        "deadline": "April 15",
    },
    "new-mexico": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("New Mexico Taxation and Revenue Department", "https://www.tax.newmexico.gov/"),
        "deadline": "April 15",
    },
    "new-york": {
        "local_tax": "New York City residents pay a city income tax on top of the state tax, and Yonkers "
                     "residents pay a surcharge. The city tax applies based on residence, not workplace - "
                     "commuting into Manhattan from outside the city does not trigger it. For a NYC "
                     "resident this is a substantial addition that the estimate below does not include.",
        "reciprocity": [],
        "payroll": [
            ("Paid Family Leave (PFL)",
             "Funded by an employee payroll deduction set annually by the state."),
            ("State Disability Insurance",
             "New York employers may deduct a small statutory weekly amount from the employee's check "
             "toward disability coverage."),
        ],
        "revenue": ("New York State Department of Taxation and Finance", "https://www.tax.ny.gov/"),
        "deadline": "April 15",
    },
    "north-carolina": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("North Carolina Department of Revenue", "https://www.ncdor.gov/"),
        "deadline": "April 15",
    },
    "north-dakota": {
        "local_tax": None,
        "reciprocity": ["Minnesota", "Montana"],
        "payroll": [],
        "revenue": ("North Dakota Office of State Tax Commissioner", "https://www.tax.nd.gov/"),
        "deadline": "April 15",
    },
    "ohio": {
        "local_tax": "Ohio has one of the densest local income tax landscapes in the country: most "
                     "municipalities levy a city income tax, and many school districts add their own. You "
                     "can owe tax to the city you work in and the city you live in, with a partial credit "
                     "between them, so an Ohio paycheck often has two or three separate local lines.",
        "reciprocity": ["Indiana", "Kentucky", "Michigan", "Pennsylvania", "West Virginia"],
        "payroll": [],
        "revenue": ("Ohio Department of Taxation", "https://tax.ohio.gov/"),
        "deadline": "April 15",
    },
    "oklahoma": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("Oklahoma Tax Commission", "https://oklahoma.gov/tax.html"),
        "deadline": "April 15",
    },
    "oregon": {
        "local_tax": "The Portland area layers additional local income taxes on top of the state tax: "
                     "Multnomah County's Preschool for All tax and Metro's Supportive Housing Services tax, "
                     "both of which apply above an income threshold.",
        "reciprocity": [],
        "payroll": [
            ("Paid Leave Oregon",
             "Funded by a payroll contribution split between employer and employee."),
        ],
        "revenue": ("Oregon Department of Revenue", "https://www.oregon.gov/dor/"),
        "deadline": "April 15",
    },
    "pennsylvania": {
        "local_tax": "Nearly every Pennsylvania municipality and school district levies a local Earned "
                     "Income Tax, commonly around 1% of gross wages and withheld by the employer. "
                     "Philadelphia instead charges its own wage tax at a much higher rate, owed by anyone "
                     "who works in the city regardless of where they live. Pennsylvania's flat state rate "
                     "looks low on its own, but the local layer is close to universal.",
        "reciprocity": ["Indiana", "Maryland", "New Jersey", "Ohio", "Virginia", "West Virginia"],
        "payroll": [
            ("Unemployment compensation (employee share)",
             "Pennsylvania withholds a small employee share of unemployment compensation tax from wages, "
             "which most states do not."),
        ],
        "revenue": ("Pennsylvania Department of Revenue", "https://www.revenue.pa.gov/"),
        "deadline": "April 15",
    },
    "rhode-island": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [
            ("Temporary Disability Insurance (TDI)",
             "Rhode Island's TDI program is funded entirely by an employee payroll deduction."),
        ],
        "revenue": ("Rhode Island Division of Taxation", "https://tax.ri.gov/"),
        "deadline": "April 15",
    },
    "south-carolina": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("South Carolina Department of Revenue", "https://dor.sc.gov/"),
        "deadline": "April 15",
    },
    "south-dakota": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("South Dakota Department of Revenue", "https://dor.sd.gov/"),
        "deadline": None,
    },
    "tennessee": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("Tennessee Department of Revenue", "https://www.tn.gov/revenue.html"),
        "deadline": None,
    },
    "texas": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("Texas Comptroller of Public Accounts", "https://comptroller.texas.gov/"),
        "deadline": None,
    },
    "utah": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("Utah State Tax Commission", "https://tax.utah.gov/"),
        "deadline": "April 15",
    },
    "vermont": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("Vermont Department of Taxes", "https://tax.vermont.gov/"),
        "deadline": "April 15",
    },
    "virginia": {
        "local_tax": None,
        "reciprocity": ["Kentucky", "Maryland", "Pennsylvania", "West Virginia"],
        "payroll": [],
        "revenue": ("Virginia Department of Taxation", "https://www.tax.virginia.gov/"),
        "deadline": "May 1",
    },
    "washington": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [
            ("Paid Family and Medical Leave (PFML)",
             "Funded by a payroll premium, part of which is withheld from the employee."),
            ("WA Cares Fund",
             "A long-term care benefit funded by an employee-only payroll deduction - unusual enough that "
             "it surprises people who move to Washington expecting no payroll tax at all."),
        ],
        "revenue": ("Washington State Department of Revenue", "https://dor.wa.gov/"),
        "deadline": None,
    },
    "west-virginia": {
        "local_tax": "Some West Virginia municipalities charge a flat city service fee on people who work "
                     "in the city, billed per week worked rather than as a percentage of pay.",
        "reciprocity": ["Kentucky", "Maryland", "Ohio", "Pennsylvania", "Virginia"],
        "payroll": [],
        "revenue": ("West Virginia Tax Division", "https://tax.wv.gov/"),
        "deadline": "April 15",
    },
    "wisconsin": {
        "local_tax": None,
        "reciprocity": ["Illinois", "Indiana", "Kentucky", "Michigan"],
        "payroll": [],
        "revenue": ("Wisconsin Department of Revenue", "https://www.revenue.wi.gov/"),
        "deadline": "April 15",
    },
    "wyoming": {
        "local_tax": None,
        "reciprocity": [],
        "payroll": [],
        "revenue": ("Wyoming Department of Revenue", "https://revenue.wyo.gov/"),
        "deadline": None,
    },
}
