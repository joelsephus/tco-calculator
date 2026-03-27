"""
TCO/ROI Formula Validation Tests

Tests all calculator formulas against known worked examples from formula-research.md.
Run with: pytest tools/validate_formulas.py -v
"""

import pytest
from dataclasses import dataclass

# ──────────────────────────────────────────────
# Formula Functions (mirror the JS calculator)
# ──────────────────────────────────────────────

def loaded_hourly_cost(base_salary: float, benefits_multiplier: float, annual_work_hours: int = 2080) -> float:
    """Fully-burdened hourly cost of an employee."""
    return (base_salary * benefits_multiplier) / annual_work_hours


def value_per_hour_from_multiplier(loaded_hourly: float, value_multiplier: float) -> float:
    """Value per hour using a multiplier on loaded cost."""
    return loaded_hourly * value_multiplier


def value_per_hour_from_revenue(annual_revenue: float, total_employees: int,
                                 utilization: float, annual_work_hours: int = 2080) -> float:
    """Value per hour using revenue-per-employee."""
    rpe = annual_revenue / total_employees
    return (rpe * utilization) / annual_work_hours


def direct_cost(loaded_hourly: float, wasted_hours: float) -> float:
    """Direct cost = loaded pay for unproductive time."""
    return loaded_hourly * wasted_hours


def opportunity_cost(value_hourly: float, loaded_hourly: float, wasted_hours: float) -> float:
    """Opportunity cost = value delta above loaded cost."""
    return (value_hourly - loaded_hourly) * wasted_hours


def total_impact(value_hourly: float, wasted_hours: float) -> float:
    """Total impact = full value of the wasted time."""
    return value_hourly * wasted_hours


def ticket_cost(customer_salary: float, support_salary: float,
                customer_minutes: float, hold_minutes: float, support_minutes: float,
                benefits_mult: float = 1.4, value_mult: float = 2.0,
                resource_cost: float = 0.0, annual_work_hours: int = 2080,
                advanced: dict | None = None) -> dict:
    """Calculate full per-ticket cost breakdown with optional advanced factors."""
    cust_loaded = loaded_hourly_cost(customer_salary, benefits_mult, annual_work_hours)
    cust_value = value_per_hour_from_multiplier(cust_loaded, value_mult)
    cust_hours = (customer_minutes + hold_minutes) / 60

    sup_loaded = loaded_hourly_cost(support_salary, benefits_mult, annual_work_hours)
    sup_value = value_per_hour_from_multiplier(sup_loaded, value_mult)
    sup_hours = support_minutes / 60

    adv = advanced or {}

    # Multi-touch and repeat contact multipliers
    avg_touches = adv.get("avg_support_touches", 1)
    fcr_rate = adv.get("first_contact_resolution_pct", 100) / 100
    repeat_mult = 1 + (1 - fcr_rate) if fcr_rate < 1 else 1

    adj_support_direct = sup_loaded * sup_hours * avg_touches * repeat_mult
    adj_support_total = sup_value * sup_hours * avg_touches * repeat_mult

    # Workaround labor
    wa_pct = adv.get("workaround_pct", 0) / 100
    wa_min = adv.get("workaround_minutes", 0)
    workaround_cost = (cust_value * wa_min / 60) * (wa_pct / (1 - wa_pct)) if wa_pct > 0 and wa_pct < 1 else 0

    # Error/rework
    err_rate = adv.get("error_rate_pct", 0) / 100
    rework_per_error = adv.get("rework_cost_per_error", 0)
    error_rework_cost = err_rate * rework_per_error

    # Management overhead
    esc_rate = adv.get("escalation_rate_pct", 0) / 100
    mgr_min = adv.get("mgr_minutes_per_escalation", 0)
    mgr_salary = adv.get("mgr_salary", 0)
    mgr_loaded = loaded_hourly_cost(mgr_salary, benefits_mult, annual_work_hours) if mgr_salary > 0 else 0
    mgr_overhead_cost = esc_rate * (mgr_loaded * mgr_min / 60)

    # Overtime/backlog
    ot_pct = adv.get("overtime_pct", 0) / 100
    ot_rate = adv.get("overtime_rate", 1.5)
    overtime_cost = cust_loaded * cust_hours * ot_pct * (ot_rate - 1) if ot_pct > 0 else 0

    advanced_total = workaround_cost + error_rework_cost + mgr_overhead_cost + overtime_cost

    return {
        "customer_direct": direct_cost(cust_loaded, cust_hours),
        "customer_opportunity": opportunity_cost(cust_value, cust_loaded, cust_hours),
        "customer_total": total_impact(cust_value, cust_hours),
        "support_direct": adj_support_direct,
        "support_opportunity": adj_support_total - adj_support_direct,
        "support_total": adj_support_total,
        "resource_cost": resource_cost,
        "workaround_cost": workaround_cost,
        "error_rework_cost": error_rework_cost,
        "mgr_overhead_cost": mgr_overhead_cost,
        "overtime_cost": overtime_cost,
        "advanced_total": advanced_total,
        "total_direct": direct_cost(cust_loaded, cust_hours) + adj_support_direct + resource_cost,
        "total_impact": total_impact(cust_value, cust_hours) + adj_support_total + resource_cost + advanced_total,
    }


def simple_payback_months(one_time_investment: float, net_annual_benefit: float) -> float:
    """Payback period in months."""
    if net_annual_benefit <= 0:
        return float('inf')
    return one_time_investment / (net_annual_benefit / 12)


def roi_percent(total_benefits: float, total_costs: float) -> float:
    """ROI as a percentage."""
    if total_costs == 0:
        return float('inf')
    return ((total_benefits - total_costs) / total_costs) * 100


def npv(initial_investment: float, annual_benefit: float, years: int, discount_rate: float = 0.08) -> float:
    """Net Present Value over N years."""
    pv_benefits = sum(annual_benefit / (1 + discount_rate) ** year for year in range(1, years + 1))
    return -initial_investment + pv_benefits


def implementation_tco_year1(software_onetime: float, services: float, first_year_licensing: float,
                              internal_hours: float, internal_loaded_hourly: float,
                              training_hours_per_person: float, num_trainees: int, trainee_loaded_hourly: float,
                              affected_employees: int, affected_loaded_hourly: float,
                              productivity_dip_pct: float, transition_weeks: int,
                              hours_per_week: float = 40) -> dict:
    """Year 1 implementation TCO with full breakdown."""
    direct_costs = software_onetime + services + first_year_licensing
    labor_cost = internal_hours * internal_loaded_hourly
    training_cost = training_hours_per_person * num_trainees * trainee_loaded_hourly
    productivity_loss = (affected_employees * affected_loaded_hourly *
                         hours_per_week * productivity_dip_pct * transition_weeks)

    total = direct_costs + labor_cost + training_cost + productivity_loss
    hidden_pct = ((training_cost + productivity_loss) / total * 100) if total > 0 else 0

    return {
        "direct_costs": direct_costs,
        "labor_cost": labor_cost,
        "training_cost": training_cost,
        "productivity_loss": productivity_loss,
        "total": total,
        "hidden_cost_pct": hidden_pct,
    }


def downtime_cost(affected_employees: int, loaded_hourly: float, downtime_hours: float,
                  annual_revenue: float = 0, annual_work_hours: int = 2080,
                  revenue_impact_pct: float = 0, recovery_costs: float = 0) -> dict:
    """Cost of a single downtime event."""
    lost_productivity = affected_employees * loaded_hourly * downtime_hours
    lost_revenue = 0
    if annual_revenue > 0:
        hourly_revenue = annual_revenue / annual_work_hours
        lost_revenue = hourly_revenue * downtime_hours * revenue_impact_pct

    total = lost_productivity + lost_revenue + recovery_costs
    return {
        "lost_productivity": lost_productivity,
        "lost_revenue": lost_revenue,
        "recovery_costs": recovery_costs,
        "total": total,
    }


# ──────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────

class TestLoadedCost:
    def test_clinical_staff(self):
        """Clinical staff at $55K with 1.4x multiplier."""
        result = loaded_hourly_cost(55000, 1.4)
        assert result == pytest.approx(37.0192, rel=1e-3)

    def test_tier1_support(self):
        """Tier 1 support at $35K with 1.4x multiplier."""
        result = loaded_hourly_cost(35000, 1.4)
        assert result == pytest.approx(23.5577, rel=1e-3)

    def test_executive(self):
        """C-Suite at $150K with 1.4x multiplier."""
        result = loaded_hourly_cost(150000, 1.4)
        assert result == pytest.approx(100.9615, rel=1e-3)

    def test_custom_hours(self):
        """Custom annual work hours (1,840 for part-time-adjusted)."""
        result = loaded_hourly_cost(50000, 1.35, 1840)
        assert result == pytest.approx(36.6848, rel=1e-3)


class TestValuePerHour:
    def test_multiplier_method(self):
        """Value per hour = loaded × 2.0."""
        loaded = loaded_hourly_cost(55000, 1.4)
        result = value_per_hour_from_multiplier(loaded, 2.0)
        assert result == pytest.approx(74.0385, rel=1e-3)

    def test_revenue_method(self):
        """Revenue-based: $5B revenue, 70K employees, 65% utilization."""
        result = value_per_hour_from_revenue(5_000_000_000, 70000, 0.65)
        assert result == pytest.approx(22.3214, rel=1e-3)

    def test_tech_company_benchmark(self):
        """Tech benchmark: $400K RPE, 75% utilization."""
        result = value_per_hour_from_revenue(400000 * 1000, 1000, 0.75)
        assert result == pytest.approx(144.2308, rel=1e-3)


class TestThreeLayerBreakdown:
    def test_no_double_counting(self):
        """Verify: direct + opportunity = total impact."""
        loaded = 37.02
        value = 74.04
        hours = 0.4167

        d = direct_cost(loaded, hours)
        o = opportunity_cost(value, loaded, hours)
        t = total_impact(value, hours)

        assert d + o == pytest.approx(t, rel=1e-4)

    def test_conservative_equals_direct(self):
        """Conservative mode = direct cost only (value = loaded)."""
        loaded = 37.02
        hours = 0.5

        d = direct_cost(loaded, hours)
        t = total_impact(loaded, hours)  # when value == loaded
        assert d == pytest.approx(t, rel=1e-4)


class TestTicketCost:
    """Tests against Example A from formula-research.md."""

    def test_example_a_customer_direct(self):
        result = ticket_cost(55000, 35000, 10, 15, 5)
        assert result["customer_direct"] == pytest.approx(15.42, rel=1e-2)

    def test_example_a_customer_opportunity(self):
        result = ticket_cost(55000, 35000, 10, 15, 5)
        assert result["customer_opportunity"] == pytest.approx(15.43, rel=1e-2)

    def test_example_a_customer_total(self):
        result = ticket_cost(55000, 35000, 10, 15, 5)
        assert result["customer_total"] == pytest.approx(30.85, rel=1e-2)

    def test_example_a_support_direct(self):
        result = ticket_cost(55000, 35000, 10, 15, 5)
        assert result["support_direct"] == pytest.approx(1.96, rel=1e-2)

    def test_example_a_support_total(self):
        result = ticket_cost(55000, 35000, 10, 15, 5)
        assert result["support_total"] == pytest.approx(3.93, rel=1e-2)

    def test_example_a_annual_impact(self):
        result = ticket_cost(55000, 35000, 10, 15, 5)
        annual = result["total_impact"] * 1904
        assert annual == pytest.approx(66221, rel=1e-2)

    def test_example_a_annual_conservative(self):
        result = ticket_cost(55000, 35000, 10, 15, 5)
        annual = result["total_direct"] * 1904
        assert annual == pytest.approx(33100, rel=1e-2)

    def test_resource_cost_included(self):
        result = ticket_cost(55000, 35000, 10, 15, 5, resource_cost=10.0)
        base = ticket_cost(55000, 35000, 10, 15, 5)
        assert result["total_impact"] == pytest.approx(base["total_impact"] + 10.0, rel=1e-4)


class TestAdvancedFactors:
    """Tests for hidden cost factors."""

    def test_no_advanced_matches_base(self):
        """With no advanced factors, results match the base calculation."""
        base = ticket_cost(55000, 35000, 10, 15, 5)
        adv = ticket_cost(55000, 35000, 10, 15, 5, advanced={})
        assert adv["total_impact"] == pytest.approx(base["total_impact"], rel=1e-6)
        assert adv["advanced_total"] == 0.0

    def test_repeat_contacts(self):
        """70% FCR increases support cost by 30%."""
        base = ticket_cost(55000, 35000, 10, 15, 5)
        result = ticket_cost(55000, 35000, 10, 15, 5,
                             advanced={"first_contact_resolution_pct": 70})
        assert result["support_total"] == pytest.approx(base["support_total"] * 1.3, rel=1e-3)

    def test_multi_touch(self):
        """2 support staff per ticket doubles support cost."""
        base = ticket_cost(55000, 35000, 10, 15, 5)
        result = ticket_cost(55000, 35000, 10, 15, 5,
                             advanced={"avg_support_touches": 2})
        assert result["support_total"] == pytest.approx(base["support_total"] * 2, rel=1e-3)

    def test_repeat_and_multitouch_compound(self):
        """FCR and multi-touch multiply together."""
        base = ticket_cost(55000, 35000, 10, 15, 5)
        result = ticket_cost(55000, 35000, 10, 15, 5,
                             advanced={"first_contact_resolution_pct": 70, "avg_support_touches": 2})
        assert result["support_total"] == pytest.approx(base["support_total"] * 2 * 1.3, rel=1e-3)

    def test_workaround_labor(self):
        """40% workaround rate, 20 min each — creates ~0.667 workarounds per ticket."""
        result = ticket_cost(55000, 35000, 10, 15, 5,
                             advanced={"workaround_pct": 40, "workaround_minutes": 20})
        # cust_value = $74.04/hr, 20 min = 0.333 hr, ratio = 0.4/0.6 = 0.667
        expected = 74.0385 * (20 / 60) * (0.4 / 0.6)
        assert result["workaround_cost"] == pytest.approx(expected, rel=1e-2)

    def test_error_rework(self):
        """5% error rate, $50 per rework = $2.50 per ticket."""
        result = ticket_cost(55000, 35000, 10, 15, 5,
                             advanced={"error_rate_pct": 5, "rework_cost_per_error": 50})
        assert result["error_rework_cost"] == pytest.approx(2.50, rel=1e-4)

    def test_management_overhead(self):
        """10% escalation, 15 min at $85K mgr salary."""
        result = ticket_cost(55000, 35000, 10, 15, 5,
                             advanced={"escalation_rate_pct": 10, "mgr_minutes_per_escalation": 15, "mgr_salary": 85000})
        mgr_loaded = loaded_hourly_cost(85000, 1.4)
        expected = 0.10 * (mgr_loaded * 15 / 60)
        assert result["mgr_overhead_cost"] == pytest.approx(expected, rel=1e-3)

    def test_overtime_backlog(self):
        """30% catch-up at 1.5x overtime."""
        result = ticket_cost(55000, 35000, 10, 15, 5,
                             advanced={"overtime_pct": 30, "overtime_rate": 1.5})
        cust_loaded = loaded_hourly_cost(55000, 1.4)
        cust_hours = 25 / 60  # 10 + 15
        expected = cust_loaded * cust_hours * 0.30 * 0.5  # (1.5 - 1) = 0.5
        assert result["overtime_cost"] == pytest.approx(expected, rel=1e-3)

    def test_advanced_total_adds_to_impact(self):
        """Advanced costs are added to total_impact."""
        base = ticket_cost(55000, 35000, 10, 15, 5)
        result = ticket_cost(55000, 35000, 10, 15, 5,
                             advanced={"error_rate_pct": 10, "rework_cost_per_error": 100})
        assert result["total_impact"] == pytest.approx(base["total_impact"] + 10.0, rel=1e-3)

    def test_all_factors_combined(self):
        """All advanced factors active at once."""
        result = ticket_cost(55000, 35000, 10, 15, 5, advanced={
            "first_contact_resolution_pct": 70,
            "avg_support_touches": 1.5,
            "workaround_pct": 30,
            "workaround_minutes": 15,
            "error_rate_pct": 5,
            "rework_cost_per_error": 50,
            "escalation_rate_pct": 15,
            "mgr_minutes_per_escalation": 20,
            "mgr_salary": 85000,
            "overtime_pct": 20,
            "overtime_rate": 1.5,
        })
        assert result["advanced_total"] > 0
        assert result["total_impact"] > result["total_direct"]
        # Support should be 1.5 touches × 1.3 repeat = 1.95x base
        base = ticket_cost(55000, 35000, 10, 15, 5)
        assert result["support_total"] == pytest.approx(base["support_total"] * 1.5 * 1.3, rel=1e-3)


class TestROI:
    def test_simple_payback(self):
        """$50K investment, $30K annual benefit = 20 months."""
        result = simple_payback_months(50000, 30000)
        assert result == pytest.approx(20.0, rel=1e-4)

    def test_payback_no_benefit(self):
        """Zero benefit = infinite payback."""
        result = simple_payback_months(50000, 0)
        assert result == float('inf')

    def test_roi_positive(self):
        """$100K benefits, $50K costs = 100% ROI."""
        result = roi_percent(100000, 50000)
        assert result == pytest.approx(100.0, rel=1e-4)

    def test_roi_negative(self):
        """$30K benefits, $50K costs = -40% ROI."""
        result = roi_percent(30000, 50000)
        assert result == pytest.approx(-40.0, rel=1e-4)

    def test_npv_positive(self):
        """$50K investment, $20K/yr for 5 years at 8% discount."""
        result = npv(50000, 20000, 5, 0.08)
        assert result == pytest.approx(29854.20, rel=1e-2)

    def test_npv_breakeven(self):
        """NPV should be near zero when benefits barely cover costs."""
        result = npv(50000, 12523, 5, 0.08)
        assert abs(result) < 100  # approximately breakeven


class TestImplementationTCO:
    """Tests against Example B from formula-research.md."""

    def test_example_b(self):
        pm_loaded = loaded_hourly_cost(85000, 1.4)
        staff_loaded = loaded_hourly_cost(55000, 1.4)

        result = implementation_tco_year1(
            software_onetime=150000,
            services=100000,
            first_year_licensing=50000,
            internal_hours=500,
            internal_loaded_hourly=pm_loaded,
            training_hours_per_person=40,
            num_trainees=200,
            trainee_loaded_hourly=staff_loaded,
            affected_employees=200,
            affected_loaded_hourly=staff_loaded,
            productivity_dip_pct=0.25,
            transition_weeks=12,
        )

        assert result["direct_costs"] == pytest.approx(300000, rel=1e-4)
        assert result["labor_cost"] == pytest.approx(28605, rel=1e-2)
        assert result["training_cost"] == pytest.approx(296154, rel=1e-2)
        assert result["productivity_loss"] == pytest.approx(888462, rel=1e-2)
        assert result["total"] == pytest.approx(1513221, rel=1e-2)
        assert result["hidden_cost_pct"] == pytest.approx(78, rel=5e-2)

    def test_five_year_tco(self):
        """5-year = year 1 + 4 × annual recurring."""
        year1_total = 1513221
        annual_recurring = 60000
        five_year = year1_total + (annual_recurring * 4)
        assert five_year == pytest.approx(1753221, rel=1e-4)


class TestDowntime:
    def test_productivity_only(self):
        """200 employees at $37.02/hr for 1 hour."""
        result = downtime_cost(200, 37.02, 1.0)
        assert result["lost_productivity"] == pytest.approx(7404, rel=1e-3)
        assert result["total"] == pytest.approx(7404, rel=1e-3)

    def test_with_revenue_loss(self):
        """Add revenue impact: $5B annual, 10% affected."""
        result = downtime_cost(200, 37.02, 1.0,
                               annual_revenue=5_000_000_000,
                               revenue_impact_pct=0.10)
        assert result["lost_revenue"] == pytest.approx(240384.62, rel=1e-2)

    def test_annualized(self):
        """4 events per year."""
        result = downtime_cost(200, 37.02, 1.0)
        annual = result["total"] * 4
        assert annual == pytest.approx(29616, rel=1e-3)

    def test_recovery_costs(self):
        """Recovery costs are additive."""
        result = downtime_cost(100, 50.0, 2.0, recovery_costs=5000)
        assert result["total"] == pytest.approx(15000, rel=1e-4)


class TestEdgeCases:
    def test_zero_salary(self):
        """$0 salary should produce $0 costs."""
        result = ticket_cost(0, 0, 10, 15, 5)
        assert result["total_impact"] == 0.0

    def test_zero_tickets(self):
        """0 annual tickets = $0 annual cost."""
        result = ticket_cost(55000, 35000, 10, 15, 5)
        assert result["total_impact"] * 0 == 0.0

    def test_zero_time(self):
        """0 minutes wasted = $0."""
        result = ticket_cost(55000, 35000, 0, 0, 0)
        assert result["total_impact"] == 0.0

    def test_no_revenue_graceful(self):
        """Revenue-based value with $0 revenue defaults cleanly."""
        result = value_per_hour_from_revenue(0, 70000, 0.65)
        assert result == 0.0

    def test_very_high_salary(self):
        """Extreme salary should still calculate correctly."""
        result = loaded_hourly_cost(500000, 1.6)
        assert result == pytest.approx(384.6154, rel=1e-3)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
