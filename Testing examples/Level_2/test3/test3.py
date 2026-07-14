# Example:3
# Adding reserve phases to the FwFm benchmark aircraft definition and running the optimization problem with Aviary.
#-- IGNORE ---

# Import Aviary API
import aviary.api as av
import sys

#import the default energy-state phase
from aviary.models.missions.energy_state_default import phase_info

# Add reserve phases to existing phase_info
phase_info.update(
    {
        'reserve_climb': {
            'subsystem_options': {'aerodynamics': {'method': 'computed'}},
            'user_options': {
                'reserve': True,
                'num_segments': 5,
                'order': 3,
                'mach_optimize': False,
                'mach_polynomial_order': 1,
                'mach_initial': (0.36, 'unitless'),
                'mach_final': (0.72, 'unitless'),
                'altitude_optimize': False,
                'altitude_polynomial_order': 1,
                'altitude_initial': (500.0, 'ft'),
                'altitude_final': (32000.0, 'ft'),
                'throttle_enforcement': 'path_constraint',
                'time_initial': (0.0, 'min'),
                'time_duration_bounds': ((30.0, 192.0), 'min'),
            },
            'initial_guesses': {
                'time': ([0, 128], 'min'),
            },
        },
        'reserve_cruise_fixed_range': {
            'subsystem_options': {'aerodynamics': {'method': 'computed'}},
            'user_options': {
                'reserve': True,
                # Distance traveled in this phase
                'target_distance': (300, 'km'),
                'num_segments': 5,
                'order': 3,
                'mach_optimize': False,
                'mach_polynomial_order': 1,
                'mach_initial': (0.72, 'unitless'),
                'mach_final': (0.72, 'unitless'),
                'altitude_optimize': False,
                'altitude_polynomial_order': 1,
                'altitude_initial': (32000.0, 'ft'),
                'altitude_final': (32000.0, 'ft'),
                'throttle_enforcement': 'boundary_constraint',
                'time_initial_bounds': ((149.5, 448.5), 'min'),
                'time_duration_bounds': ((0, 300), 'min'),
            },
            'initial_guesses': {
                'time': ([30, 120], 'min'),
            },
        },
        'reserve_cruise_fixed_time': {
            'subsystem_options': {'aerodynamics': {'method': 'computed'}},
            'user_options': {
                'reserve': True,
                # Time length of this phase
                'time_duration': (30, 'min'),
                'num_segments': 5,
                'order': 3,
                'distance_solve_segments': False,
                'mach_optimize': False,
                'mach_polynomial_order': 1,
                'mach_initial': (0.72, 'unitless'),
                'mach_final': (0.72, 'unitless'),
                'altitude_optimize': False,
                'altitude_polynomial_order': 1,
                'altitude_initial': (32000.0, 'ft'),
                'altitude_final': (32000.0, 'ft'),
                'throttle_enforcement': 'boundary_constraint',
                'time_initial_bounds': ((60, 448.5), 'min'),
            },
        },
        'reserve_descent': {
            'subsystem_options': {'aerodynamics': {'method': 'computed'}},
            'user_options': {
                'reserve': True,
                'num_segments': 5,
                'order': 3,
                'mach_optimize': False,
                'mach_polynomial_order': 1,
                'mach_initial': (0.72, 'unitless'),
                'mach_final': (0.36, 'unitless'),
                'altitude_optimize': False,
                'altitude_polynomial_order': 1,
                'altitude_initial': (32000.0, 'ft'),
                'altitude_final': (500.0, 'ft'),
                'throttle_enforcement': 'path_constraint',
                'time_initial_bounds': ((120.5, 550.0), 'min'),
                'time_duration_bounds': ((29.0, 87.0), 'min'),
            },
        },
    }
)

prob = av.run_aviary(
        aircraft_data='models/aircraft/advanced_single_aisle/advanced_single_aisle_FLOPS.csv',
        phase_info=phase_info,
    )