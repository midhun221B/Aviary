# Running sizing mission, then run two off-design missions (one for max range and one for min fuel).

import aviary.api as av
from pathlib import Path

# Phase info
phase_info = av.default_energy_state_phase_info
phase_info['post_mission']['target_range'] = (2500.0, 'nmi')

# ============================================================
# Sizing Mission
# ============================================================
design_prob = av.run_aviary(
    aircraft_data='models/aircraft/advanced_single_aisle/advanced_single_aisle_FLOPS.csv',
    phase_info=phase_info,
    verbosity=1,
)

# ============================================================
# OFF_DESIGN_MAX_RANGE Mission
# ============================================================
off_design_max_range_prob = design_prob.run_off_design_mission(
    problem_type='off_design_max_range',
    mission_gross_mass=115000,
    name='off_design_max_range_mission',
)

# ============================================================
# OFF_DESIGN_MIN_FUEL Mission
# ============================================================
off_design_min_fuel_prob = design_prob.run_off_design_mission(
    problem_type='off_design_min_fuel',
    mission_range=1250,
    name='off_design_min_fuel_mission',
)


# ============================================================
# SUMMARY PRINTER
# ============================================================
def print_sizing_results(prob, label):
    def gv(var, units):
        try:
            return prob.get_val(var, units=units)[0]
        except Exception:
            return None

    design_range         = gv('aircraft:design:range', 'nmi')
    mission_range        = gv('state_output.range_final', 'nmi')
    fuel_mass            = gv('pre_mission.total_fuel_mass_comp.total_fuel_mass', 'lbm')
    oem                  = gv('mission:operating_mass', 'lbm')
    payload              = gv('aircraft:crew_and_payload:total_payload_mass', 'lbm')
    design_gross_mass    = gv('aircraft:design:gross_mass', 'lbm')
    mission_gross_mass   = gv('takeoff_mass_comp.gross_mass', 'lbm')  # actual flown mass this mission

    print(f"\n{label} Results")
    print("-" * len(f"{label} Results"))
    print(f"Design Range = {design_range} nmi")
    print(f"Mission Range = {mission_range} nmi")
    print(f"Fuel Mass = {fuel_mass} lbm")
    print(f"Operating Empty Mass = {oem} lbm")
    print(f"Payload Mass = {payload} lbm")
    print(f"Design Gross Mass = {design_gross_mass} lbm")
    print(f"Mission Gross Mass = {mission_gross_mass} lbm")


print_sizing_results(design_prob, "Sizing")
print_sizing_results(off_design_max_range_prob, "OFF_DESIGN_MAX_RANGE")
print_sizing_results(off_design_min_fuel_prob, "OFF_DESIGN_MIN_FUEL")
