# Run 4 cases to compare the effect of changing the aircraft's wing aspect ratio on the optimization results.

import aviary.api as av  # type: ignore
import csv
import os

# ============================================================
# STEP 1: Create the modified aircraft CSV (aspect_ratio - 0.2)
# ============================================================
filename = 'validation_cases/validation_data/test_models/aircraft_for_bench_FwFm.csv'
filename = av.get_path(filename)

with open(filename, 'r') as file:
    reader = csv.reader(file)
    lines = list(reader)

index = None
for i, line in enumerate(lines):
    if 'aircraft:wing:aspect_ratio' in line:
        index = i
        break

if index is not None:
    aspect_ratio = float(lines[index][1]) - 0.2
    lines[index][1] = str(aspect_ratio)
else:
    print("WARNING: 'aircraft:wing:aspect_ratio' not found — writing file unmodified.")

new_filename = os.path.join(os.path.dirname(__file__), 'aircraft_for_bench_FwFm_modified.csv')

with open(new_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(lines)

print(f"Modified aircraft file written to: {new_filename}\n")


# ============================================================
# STEP 2: Define phase_info (shared baseline, order = 1)
# ============================================================
def make_phase_info(poly_order_climb_descent=1):
    phase_info = {
        'pre_mission': {'include_takeoff': False, 'optimize_mass': True},
        'climb_1': {
            'subsystem_options': {'aerodynamics': {'method': 'computed'}},
            'user_options': {
                'num_segments': 3,
                'order': 3,
                'distance_solve_segments': False,
                'mach_optimize': True,
                'mach_polynomial_order': poly_order_climb_descent,
                'mach_initial': (0.2, 'unitless'),
                'mach_final': (0.72, 'unitless'),
                'mach_bounds': ((0.18, 0.74), 'unitless'),
                'altitude_optimize': False,
                'altitude_polynomial_order': poly_order_climb_descent,
                'altitude_initial': (0.0, 'ft'),
                'altitude_final': (30500.0, 'ft'),
                'altitude_bounds': ((0.0, 31000.0), 'ft'),
                'throttle_enforcement': 'path_constraint',
                'time_initial_bounds': ((0.0, 0.0), 'min'),
                'time_duration_bounds': ((27.0, 81.0), 'min'),
            },
            'initial_guesses': {'time': ([0, 54], 'min')},
        },
        'cruise': {
            'subsystem_options': {'aerodynamics': {'method': 'computed'}},
            'user_options': {
                'num_segments': 3,
                'order': 3,
                'mach_optimize': True,
                'mach_polynomial_order': 1,
                'mach_initial': (0.72, 'unitless'),
                'mach_final': (0.72, 'unitless'),
                'mach_bounds': ((0.7, 0.74), 'unitless'),
                'altitude_optimize': False,
                'altitude_initial': (30500.0, 'ft'),
                'altitude_final': (31000.0, 'ft'),
                'altitude_bounds': ((30000.0, 31500.0), 'ft'),
                'throttle_enforcement': 'boundary_constraint',
                'time_initial_bounds': ((27.0, 81.0), 'min'),
                'time_duration_bounds': ((85.5, 256.5), 'min'),
            },
            'initial_guesses': {'time': ([54, 171], 'min')},
        },
        'descent_1': {
            'subsystem_options': {'aerodynamics': {'method': 'computed'}},
            'user_options': {
                'num_segments': 3,
                'order': 3,
                'mach_optimize': True,
                'mach_polynomial_order': poly_order_climb_descent,
                'mach_initial': (0.72, 'unitless'),
                'mach_final': (0.2, 'unitless'),
                'mach_bounds': ((0.18, 0.74), 'unitless'),
                'altitude_optimize': False,
                'altitude_polynomial_order': poly_order_climb_descent,
                'altitude_initial': (31000.0, 'ft'),
                'altitude_final': (500.0, 'ft'),
                'altitude_bounds': ((0.0, 31500.0), 'ft'),
                'throttle_enforcement': 'path_constraint',
                'time_initial_bounds': ((112.5, 337.5), 'min'),
                'time_duration_bounds': ((26.5, 79.5), 'min'),
            },
            'initial_guesses': {'time': ([225, 53], 'min')},
        },
        'post_mission': {
            'include_landing': False,
            'constrain_range': True,
            'target_range': (1915, 'nmi'),
        },
    }
    return phase_info


# ============================================================
# STEP 3: Helper to run + extract summary
# ============================================================
def run_case(aircraft_data, poly_order, label):
    print(f"\n{'='*60}\nRUNNING CASE: {label}\n{'='*60}")
    phase_info = make_phase_info(poly_order_climb_descent=poly_order)
    prob = av.run_aviary(aircraft_data=aircraft_data, phase_info=phase_info)

    fuel_mass = prob.get_val(av.Mission.FUEL_MASS, units='kg')[0]

    print(f"\n--- {label} SUMMARY ---")
    print(f"Fuel mass : {fuel_mass:.2f} kg")

    return {'label': label, 'fuel_mass_kg': fuel_mass}


# ============================================================
# STEP 4: Run all cases
# ============================================================
results = []

# Case A: baseline aircraft, order=1 (your original)
results.append(run_case(filename, poly_order=1, label='Baseline aircraft, order=1'))

# Case B: baseline aircraft, order=3 (polynomial order effect only)
results.append(run_case(filename, poly_order=3, label='Baseline aircraft, order=3'))

# Case C: modified aircraft (AR-0.2), order=1 (aspect ratio effect only)
results.append(run_case(new_filename, poly_order=1, label='Modified aircraft (AR-0.2), order=1'))

# Case D: modified aircraft (AR-0.2), order=3 (combined effect)
results.append(run_case(new_filename, poly_order=3, label='Modified aircraft (AR-0.2), order=3'))


# ============================================================
# STEP 5: Print comparison table
# ============================================================
print(f"\n{'='*60}\nCOMPARISON TABLE\n{'='*60}")
print(f"{'Case':<40}{'Fuel Mass (kg)':>15}")
print('-'*60)
for r in results:
    print(f"{r['label']:<40}{r['fuel_mass_kg']:>15.2f}")

