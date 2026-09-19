"""Shared engineering model functions for Trividya-Loop baseline v1.0."""
import math
G = 9.80665
SIGMA = 5.670374419e-8

def rho_air(P_Pa, T_K, R=287.0):
    return P_Pa / (R * T_K)

def speed_of_sound(T_K, gamma=1.4, R=287.0):
    return math.sqrt(gamma * R * T_K)

def drag_force(v, rho, Cd, A):
    return 0.5 * rho * Cd * A * v * v

def trip_profile(L_m, v_c, a, j):
    """Jerk-limited acceleration profile timing (analytic).
    Returns dict with t_accel, d_accel, t_cruise, d_cruise, t_total for accel-cruise-brake."""
    # time to ramp accel to a at jerk j
    t_j = a / j
    # velocity gained during jerk ramps (both ends): a*t_j ; distance during ramp approx
    # simplified trapezoidal accel: v_c = a * (t_a - t_j) -> t_a = v_c/a + t_j
    t_a = v_c / a + t_j
    d_a = 0.5 * v_c * (t_a + t_j) / 1.0 * 0 + (v_c**2) / (2*a) + 0.5 * v_c * t_j  # distance accel incl jerk ramp
    if 2 * d_a >= L_m:
        # never reaches cruise (short trip) - triangular profile
        v_peak = math.sqrt(a * L_m / (1 + a * t_j / v_c)) if False else math.sqrt(2 * a * L_m / 2)
        v_peak = math.sqrt(a * L_m)  # symmetric accel/decel approx
        t_a2 = v_peak / a + t_j
        return dict(t_accel=t_a2, d_accel=L_m/2, t_cruise=0.0, d_cruise=0.0,
                    t_total=2*t_a2, v_peak=v_peak)
    d_c = L_m - 2 * d_a
    t_c = d_c / v_c
    return dict(t_accel=t_a, d_accel=d_a, t_cruise=t_c, d_cruise=d_c,
                t_total=2*t_a + t_c, v_peak=v_c)

def stop_distance(v, a_e):
    return v*v / (2*a_e)

def stop_time(v, a_e):
    return v / a_e

def radiative_W(Ts_K, Tt_K, eps, A):
    return eps * SIGMA * A * (Ts_K**4 - Tt_K**4)
