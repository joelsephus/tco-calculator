# TCO/ROI Formula Research

Compiled from Gartner, Forrester TEI methodology, Nielsen Norman Group, and industry benchmarks.
Last updated: 2026-03-27

---

## 1. Core Cost Engine

These formulas are shared across all calculator modes.

### 1.1 Loaded Employee Cost

The fully-burdened cost of an employee, including salary, benefits, taxes, and overhead.

```
Loaded Annual Cost = Base Salary × Benefits Multiplier
Loaded Hourly Cost = Loaded Annual Cost / Annual Work Hours
```

**Benefits Multiplier ranges (industry standard):**
| Workforce Type | Multiplier Range | Recommended Default |
|---|---|---|
| General workforce | 1.25x – 1.40x | 1.35x |
| IT/Technical roles | 1.40x – 1.60x | 1.50x |
| Healthcare (clinical) | 1.30x – 1.45x | 1.40x |
| Professional services | Up to 2.70x | N/A (billable model) |

**What the multiplier covers:**
- Health insurance, dental, vision
- 401(k)/retirement contributions
- FICA, unemployment insurance, workers comp
- Office space, utilities, equipment
- Software licenses, training budget

**Sources:**
- Nielsen Norman Group: "Loaded Cost of Employee Time"
- Xantrion: "How Much Is Your Employees' Time Truly Worth"

### 1.2 Value Per Hour (Revenue-Based)

The economic value an employee generates per hour of productive work.

```
Revenue Per Employee = Annual Org Revenue / Total Employees
Value Per Hour = (Revenue Per Employee × Billable Utilization %) / Annual Work Hours
```

**Industry benchmarks:**
| Industry | Revenue Per Employee | Value Per Hour (est.) |
|---|---|---|
| Software/Tech | $400,000 | $185 – $250 |
| Healthcare services | $80,000 – $150,000 | $37 – $70 |
| Behavioral health/nonprofit | $50,000 – $100,000 | $23 – $47 |
| Professional services | $150,000 – $300,000 | $70 – $140 |

**Billable utilization** = % of work hours spent on revenue-generating activity.
- Healthcare: 60–75% (clinical staff), 40–60% (admin)
- Default for mixed workforce: 65%

**Sources:**
- Finmark: "Revenue Per Employee"
- AIHR: "Calculating Revenue Per Employee"
- Scoro: "Revenue Per Employee for Service Firms"

### 1.3 The Three-Layer Cost Breakdown

Every cost output uses this consistent structure to avoid double-counting:

```
Direct Cost      = Loaded Hourly Cost × Wasted Hours
Opportunity Cost = (Value Per Hour − Loaded Hourly Cost) × Wasted Hours
Total Impact     = Direct Cost + Opportunity Cost
                 = Value Per Hour × Wasted Hours
```

**Why this matters:**
- Direct Cost = what you **paid** for unproductive time (salary still going out)
- Opportunity Cost = the **additional** value lost beyond compensation (the delta)
- Total Impact = the full value that hour would have generated

**If revenue data is unavailable**, use a value multiplier instead:
```
Value Per Hour = Loaded Hourly Cost × Value Multiplier
```
Recommended value multiplier for healthcare: 1.5x – 2.5x loaded cost (default: 2.0x)

### 1.4 Two Estimation Modes

| Mode | Formula | Use Case |
|---|---|---|
| **Conservative** | Total = Loaded Hourly Cost × Hours | Formal business cases, budget requests |
| **Full Impact** | Total = Value Per Hour × Hours | Strategic analysis, true organizational impact |

The calculator should always show both, with conservative as the default for export.

---

## 2. Recurring Issue Cost (Tab 1)

For calculating the ongoing cost of IT help desk tickets, recurring problems, or process inefficiencies.

### 2.1 Per-Ticket Cost

```
Customer Cost Per Ticket:
  customer_hourly = (customer_salary × benefits_multiplier) / annual_work_hours
  customer_value_hourly = customer_hourly × value_multiplier  (or use RPE-based value/hr)
  wasted_hours = (active_minutes + hold_minutes) / 60

  direct_cost = customer_hourly × wasted_hours
  opportunity_cost = (customer_value_hourly − customer_hourly) × wasted_hours
  total_customer_impact = customer_value_hourly × wasted_hours

Support Cost Per Ticket:
  support_hourly = (support_salary × benefits_multiplier) / annual_work_hours
  support_value_hourly = support_hourly × value_multiplier
  support_wasted_hours = support_minutes / 60

  direct_cost = support_hourly × support_wasted_hours
  opportunity_cost = (support_value_hourly − support_hourly) × support_wasted_hours
  total_support_impact = support_value_hourly × support_wasted_hours

Total Per Ticket = total_customer_impact + total_support_impact + resource_cost_per_ticket
```

**Note:** The existing calculator applied a "tier multiplier" to support costs. This is replaced by using the actual support staff salary for each tier — the salary IS the tier difference. The tier multiplier was double-counting the seniority cost.

### 2.2 Annual Cost

```
Annual Cost = Total Per Ticket × Annual Ticket Volume
```

### 2.3 Sensitivity Analysis

```
Savings at X% Reduction = Annual Cost × (X / 100)
Break-Even Investment (1 year) = Annual Cost × Expected Reduction %
Break-Even Investment (N years) = Annual Cost × Expected Reduction % × N
```

### 2.4 Context-Switching Adder (Optional)

Research shows it takes ~23 minutes to regain full focus after an interruption (University of California, Irvine). For knowledge workers, add this to the customer's wasted time:

```
Adjusted Customer Time = Active Minutes + Hold Minutes + Context Switch Penalty (default: 15 min)
```

The 15-minute default is conservative (research says 23 min). Users can adjust.

**Source:** Mark, Gonzalez & Harris (2005). "No Task Left Behind?"

### 2.5 Advanced Hidden Cost Factors (Optional)

These factors capture costs that are typically invisible in standard TCO analysis. Each is added to the per-ticket total.

#### 2.5.1 Repeat Contacts (First Contact Resolution)

Many tickets don't resolve on first contact, generating callbacks and follow-ups:
```
Repeat Multiplier = 1 + (1 − FCR Rate)
Adjusted Support Cost = Base Support Cost × Repeat Multiplier

Example: 70% FCR → Repeat Multiplier = 1.30, so support cost increases by 30%
```

**Industry benchmark:** Average help desk FCR rate is 70-75% (HDI).

#### 2.5.2 Multi-Touch Support

A single ticket may involve multiple support staff (L1 takes call, L2 remotes in, L3 investigates):
```
Multi-Touch Multiplier = Average Support Staff per Ticket
Adjusted Support Cost = Base Support Cost × Multi-Touch Multiplier × Repeat Multiplier
```

#### 2.5.3 Workaround Labor

People who hit the same issue but don't call the help desk — they just work around it manually. This is invisible ticket volume:
```
Workaround Cost per Ticket = (Customer Value/Hr × Workaround Minutes / 60) × (Workaround % / (100% − Workaround %))

Example: If 40% of affected users work around the issue for 20 min each,
  and your ticket count represents the 60% who do call:
  Ratio = 0.40 / 0.60 = 0.667 workaround instances per ticket
  Cost = $74.04/hr × (20/60) × 0.667 = $16.45 per ticket
```

#### 2.5.4 Error/Rework Costs

Downstream errors caused by the issue (wrong billing codes, duplicate data, incorrect documentation):
```
Error/Rework Cost per Ticket = Error Rate % × Average Rework Cost per Error

Healthcare benchmark: Claim rework costs $25–$118 per rejected claim (MGMA, HFMA)
```

#### 2.5.5 Management Overhead

Supervisor time on escalations, exceptions, workarounds, and complaints:
```
Mgmt Overhead per Ticket = Escalation Rate % × (Manager Loaded Hourly × Manager Minutes / 60)
```

#### 2.5.6 Overtime/Backlog

Work that didn't happen during the disruption still needs to get done, often at overtime rates:
```
Overtime Cost per Ticket = Customer Loaded Hourly × Customer Wasted Hours × Catch-Up % × (Overtime Rate − 1)

Default overtime rate: 1.5x (FLSA standard)
```

#### 2.5.7 Combined Formula

```
Total Per Ticket = Customer Impact + Adjusted Support Impact + Resource Cost
                 + Workaround Cost + Error/Rework Cost + Mgmt Overhead + Overtime Cost
```

---

## 3. Improvement ROI (Tab 2)

For calculating the return on investing in a solution to a known problem.

### 3.1 Annual Savings

```
Annual Savings = Current Annual Cost × Expected Improvement %
Net Annual Benefit = Annual Savings − Annual Recurring Cost of Solution
```

### 3.2 Simple Payback Period

```
Payback Period (months) = One-Time Investment / (Net Annual Benefit / 12)
```

### 3.3 Return on Investment

```
ROI % = ((Total Benefits over N years − Total Costs over N years) / Total Costs) × 100

Where:
  Total Benefits = Annual Savings × N years  (gross savings, before recurring costs)
  Total Costs = One-Time Investment + (Annual Recurring Cost × N years)
```

### 3.4 Net Present Value (NPV)

Accounts for the time value of money. A dollar saved next year is worth less than a dollar saved today.

```
NPV = −Initial Investment + Σ (Net Annual Benefit / (1 + discount_rate)^year)
    for year = 1 to N

Default discount rate: 8% (typical for corporate capital budgeting)
```

### 3.5 Confidence-Adjusted Estimates

Apply a confidence factor to account for estimation uncertainty:

```
Adjusted Improvement % = Expected Improvement % × Confidence Factor

Where Confidence Factor:
  Conservative: 0.6
  Moderate: 0.8
  Aggressive: 1.0
```

---

## 4. Implementation TCO (Tab 3)

For calculating the total cost of implementing a new system or major change.

### 4.1 Year 1 TCO

```
Year 1 TCO = Direct Costs + Labor Costs + Productivity Loss Costs

Direct Costs:
  Software/Hardware (one-time) + Implementation Services + First Year Licensing

Labor Costs:
  Internal Staff Hours × Loaded Hourly Cost (for each role involved)

Productivity Loss (Learning Curve):
  Affected Employees × Loaded Hourly Cost × Weekly Hours Lost × Weeks of Transition

  OR using percentage method:
  Affected Employees × Loaded Hourly Cost × Annual Work Hours × Productivity Dip % × (Transition Weeks / 52)

Training Cost:
  Training Hours per Employee × Number of Employees × Loaded Hourly Cost
```

### 4.2 Ongoing Annual TCO (Year 2+)

```
Annual TCO = Recurring Licensing + Support/Maintenance + Ongoing Training + Internal Support FTE
```

### 4.3 Multi-Year Total

```
5-Year TCO = Year 1 TCO + (Annual TCO × 4)
```

### 4.4 Hidden Cost Ratio

```
Hidden Cost % = (Productivity Loss + Training Cost) / Total Year 1 TCO × 100
```

Research shows this is typically 40–60% of total implementation cost, but most business cases only account for direct costs.

**Sources:**
- NetSuite: "ERP TCO"
- JumpCloud: "5 Things to Consider When Calculating IT TCO"
- EHR in Practice: "Lost Productivity"

---

## 5. Downtime Cost (Tab 4)

For calculating the cost of system outages or service disruptions.

### 5.1 Per-Event Cost

```
Lost Productivity = Affected Employees × Loaded Hourly Cost × Downtime Hours
Lost Revenue = (Annual Revenue / Annual Work Hours) × Downtime Hours × Revenue Impact %
Recovery Costs = Overtime + Emergency Vendor + Other (user-entered)
Total Event Cost = Lost Productivity + Lost Revenue + Recovery Costs
```

### 5.2 Including Opportunity Cost

```
Full Impact = Affected Employees × Value Per Hour × Downtime Hours + Lost Revenue + Recovery
```

### 5.3 Annualized Cost

```
Annual Downtime Cost = Total Event Cost × Expected Events Per Year
```

### 5.4 Industry Benchmarks

| Company Size | Cost Per Minute | Cost Per Hour |
|---|---|---|
| Small business | $427 | $25,620 |
| Medium business | $9,000 | $540,000 |
| Enterprise | Varies | $300,000+ (Gartner avg) |

**Healthcare-specific:** 44% of organizations report downtime costs exceeding $1M/hour when including compliance penalties and patient safety risk.

**Sources:**
- Gartner (2014, updated): Average cost of downtime
- Atlassian: "Calculating Cost of Downtime"
- ConnectWise: "How to Calculate Cost of Downtime"
- HappySignals: "Lost Time is Lost Money" (3.22 hours perceived lost per IT incident)

---

## 6. Additional Cost Factors

### 6.1 Ripple/Cascade Effect

When one person's downtime blocks others:
```
Cascade Multiplier = 1 + (Number of Blocked Employees / Directly Affected Employees)
Adjusted Affected = Directly Affected × Cascade Multiplier
```

### 6.2 Morale/Attrition Cost (Optional)

Chronic issues increase turnover. Replacement cost:
```
Replacement Cost = Annual Salary × Replacement Multiplier

Replacement Multiplier:
  Entry level: 0.5x
  Mid-level: 1.0x – 1.5x
  Senior/specialized: 2.0x
```

**Sources:** SHRM, Work Institute retention studies

### 6.3 Compliance/Regulatory Risk (Healthcare)

In healthcare, downtime can affect:
- Documentation timeliness (billing compliance)
- Medication administration records
- Incident reporting deadlines

These are quantifiable as potential penalty costs but highly variable. Include as a user-entered optional field.

### 6.4 Cost of Poor Quality (COPQ) Benchmarks

For contextualizing results:
- Healthy organizations: 10–15% of operational costs
- Organizations with poor systems: 20–40% of sales
- A 24% decrease in COPQ → 17% increase in labor productivity, 11% improvement in profitability

**Sources:**
- IDEAGEN: "COPQ Ultimate Guide"
- SixSigma Daily: "Cost of Poor Quality"

---

## 7. Worked Examples

### Example A: Help Desk Ticket (Recurring Issue)

**Scenario:** Clinical staff member calls about Avatar access issues
- Customer: Clinical Staff, $55,000 salary
- Hold time: 15 min, Active time: 10 min
- Support: Tier 1, $35,000 salary, 5 min resolution
- Annual tickets: 1,904
- Benefits multiplier: 1.4x, Value multiplier: 2.0x

**Calculation:**
```
Customer loaded hourly = ($55,000 × 1.4) / 2,080 = $37.02/hr
Customer value hourly = $37.02 × 2.0 = $74.04/hr
Customer wasted hours = 25 min / 60 = 0.4167 hr

Customer direct cost = $37.02 × 0.4167 = $15.42
Customer opportunity cost = ($74.04 − $37.02) × 0.4167 = $15.43
Customer total impact = $74.04 × 0.4167 = $30.85

Support loaded hourly = ($35,000 × 1.4) / 2,080 = $23.56/hr
Support value hourly = $23.56 × 2.0 = $47.12/hr
Support wasted hours = 5 min / 60 = 0.0833 hr

Support direct cost = $23.56 × 0.0833 = $1.96
Support opportunity cost = ($47.12 − $23.56) × 0.0833 = $1.96
Support total impact = $47.12 × 0.0833 = $3.93

Per-ticket total impact = $30.85 + $3.93 = $34.78
Annual total impact = $34.78 × 1,904 = $66,221

Conservative (loaded cost only):
Per-ticket = $15.42 + $1.96 = $17.38
Annual = $17.38 × 1,904 = $33,100
```

### Example B: System Implementation TCO

**Scenario:** New scheduling system for 200 clinical staff
- Software: $150,000 (one-time) + $50,000/year
- Implementation services: $100,000
- Internal PM time: 500 hours at $85,000 salary
- Training: 40 hours × 200 employees at avg $55,000 salary
- Productivity dip: 25% for 12 weeks, 200 employees

**Calculation:**
```
PM loaded hourly = ($85,000 × 1.4) / 2,080 = $57.21/hr
PM labor cost = 500 × $57.21 = $28,605

Staff loaded hourly = ($55,000 × 1.4) / 2,080 = $37.02/hr
Training cost = 40 × 200 × $37.02 = $296,154

Productivity dip cost = 200 × $37.02 × (40 hrs/week × 0.25) × 12 weeks
                      = 200 × $37.02 × 10 × 12 = $888,462

Year 1 TCO = $150,000 + $100,000 + $50,000 + $28,605 + $296,154 + $888,462
           = $1,513,221

Ongoing Annual = $50,000 (licensing) + $10,000 (support) = $60,000
5-Year TCO = $1,513,221 + ($60,000 × 4) = $1,753,221

Hidden cost ratio = ($296,154 + $888,462) / $1,513,221 = 78%
```

This example illustrates the plan's key point: the apparent cost ($300,000 for software + services) is only 20% of the true Year 1 TCO.
