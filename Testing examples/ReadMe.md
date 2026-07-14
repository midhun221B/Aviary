Examples for learning Aviary

/Test_1: Simple example case running "Advanced Single Aisle” 

/Test_2: Aviary's FwFm — "Flops with Flops mission" — benchmark validation aircraft, a single-aisle transport. Simultaneous trajectory + sizing optimization. Two constraints to meet:
- Thrust-to-Weight ratio greater than 0.35
- Wing loading greater than 120 lbf./ft.2

/Test_3: Adding reserve phases to the FwFm benchmark aircraft definition and running the optimization problem with Aviary.

/Test_4: Modify the phase_info object from our prior example by increasing num_segments to 3 and setting mach_optimize to True in each of the three phases. This means that we’ll query the aircraft performance at more points along the mission and also give the optimizer the freedom to choose an optimal Mach profile.