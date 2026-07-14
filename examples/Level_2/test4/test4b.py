# Modified version of test4.py to test the effect of changing the aircraft's wing aspect ratio on the optimization results.

import aviary.api as av # type: ignore
import csv
import os

# -- MODIFY CSV FILE ---
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

print(f"Modified aircraft file written to: {new_filename}")

# -- RUN AVIARY WITH MODIFIED AIRCRAFT ---
phase_info = {
    'pre_mission': {'include_takeoff': False, 'optimize_mass': True},
    'climb': {
        'subsystem_options': {'aerodynamics': {'method': 'computed'}},
        'user_options': {
            'num_segments': 5,
            'order': 3,
            'mach_optimize': True,
            'mach_polynomial_order': 1,
            'mach_initial': (0.2, 'unitless'),
            'mach_final': (0.72, 'unitless'),
            'mach_bounds': ((0.18, 0.74), 'unitless'),
            'altitude_optimize': False,
            'altitude_initial': (0.0, 'ft'),
            'altitude_final': (32000.0, 'ft'),
            'altitude_bounds': ((0.0, 32000.0), 'ft'),
            'throttle_enforcement': 'path_constraint',
            'time_initial_bounds': ((0.0, 0.0), 'min'),
            'time_duration_bounds': ((27.0, 81.0), 'min'),
        },
        'initial_guesses': {'time': ([0, 40], 'min')},
    },
    'cruise': {
        'subsystem_options': {'aerodynamics': {'method': 'computed'}},
        'user_options': {
            'num_segments': 1,
            'order': 3,
            'mach_optimize': True,
            'mach_polynomial_order': 1,
            'mach_initial': (0.72, 'unitless'),
            'mach_final': (0.72, 'unitless'),
            'mach_bounds': ((0.7, 0.74), 'unitless'),
            'altitude_optimize': False,
            'altitude_initial': (32000.0, 'ft'),
            'altitude_final': (32000.0, 'ft'),
            'altitude_bounds': ((32000.0, 32000.0), 'ft'),
            'throttle_enforcement': 'boundary_constraint',
            'time_initial_bounds': ((27.0, 81.0), 'min'),
            'time_duration_bounds': ((85.0, 300.0), 'min'),
        },
        'initial_guesses': {'time': ([40, 150], 'min')},
    },
    'descent': {
        'subsystem_options': {'aerodynamics': {'method': 'computed'}},
        'user_options': {
            'num_segments': 5,
            'order': 3,
            'mach_optimize': True,
            'mach_polynomial_order': 1,
            'mach_initial': (0.72, 'unitless'),
            'mach_final': (0.2, 'unitless'),
            'mach_bounds': ((0.18, 0.74), 'unitless'),
            'altitude_optimize': False,
            'altitude_initial': (32000.0, 'ft'),
            'altitude_final': (500.0, 'ft'),
            'altitude_bounds': ((0.0, 32000.0), 'ft'),
            'throttle_enforcement': 'path_constraint',
            'time_initial_bounds': ((112.0, 381.0), 'min'),
            'time_duration_bounds': ((26.5, 79.5), 'min'),
        },
        'initial_guesses': {'time': ([190, 50], 'min')},
    },
    'post_mission': {
        'include_landing': False,
        'constrain_range': True,
        'target_range': (1915, 'nmi'),
    },
}

# Run Aviary with the modified aircraft file and the defined phase information
prob = av.run_aviary(
    aircraft_data=new_filename,
    phase_info=phase_info,
)

# -- SUMMARY OUTPUT ---
print("\n" + "="*50)
print("MISSION SUMMARY")
print("="*50)
print(f"Fuel mass         : {prob.get_val(av.Mission.FUEL_MASS, units='kg')[0]:.2f} kg")
print("="*50)