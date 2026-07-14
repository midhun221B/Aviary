# Modify the phase_info object from our prior example by increasing num_segments to 3 and setting mach_optimize to True in each of the three phases.
#-- IGNORE ---
#Import Aviary API
import aviary.api as av # type: ignore

#Phase_info
phase_info = {
    'pre_mission': {'include_takeoff': False, 'optimize_mass': True},
    'climb_1': {
        'subsystem_options': {'aerodynamics': {'method': 'computed'}},
        'user_options': {
            'num_segments': 3,
            'order': 3,
            'distance_solve_segments': False,
            'mach_optimize': True,
            'mach_polynomial_order': 1,
            'mach_initial': (0.2, 'unitless'),
            'mach_final': (0.72, 'unitless'),
            'mach_bounds': ((0.18, 0.74), 'unitless'),
            'altitude_optimize': False,
            'altitude_polynomial_order': 1,
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
            'mach_polynomial_order': 1,
            'mach_initial': (0.72, 'unitless'),
            'mach_final': (0.2, 'unitless'),
            'mach_bounds': ((0.18, 0.74), 'unitless'),
            'altitude_optimize': False,
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

#-- RUN AVIARY ---
prob = av.run_aviary(
        aircraft_data='models/aircraft/advanced_single_aisle/advanced_single_aisle_FLOPS.csv',
        phase_info=phase_info,
    )