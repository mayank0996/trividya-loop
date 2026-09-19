"""EXP-1: Full-route time-stepped trajectory simulation (accel-cruise-brake).
MODEL OUTPUT - simulated, not physical test data."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, json, csv
from model import rho_air, drag_force

L   = 1450e3          # route length [m]
VC  = 1165/3.6        # cruise speed [m/s]
A   = 1.0             # accel [m/s2]
J   = 0.5             # jerk [m/s3]
AE  = 1.0             # service decel [m/s2]
M   = 750.0           # pod mass [kg]
RHO = rho_air(100.0, 300.0)
CD, AF = 0.3, 1.327
ETA, REGEN = 0.90, 0.60
P_LEV = 1.0 * 0.75    # kW (1 kW/t * 0.75 t)
P_AUX = 1.0           # kW

dt = 0.5
t, v, x, a = 0.0, 0.0, 0.0, 0.0
rows = []
E_prop = E_lev = E_aux = E_regen = 0.0
phase = "accel"
tj = A / J
# pre-compute accel distance with jerk ramps
d_acc = VC**2/(2*A) + 0.5*VC*tj
d_brk = VC**2/(2*AE) + 0.5*VC*(AE/J)
d_cruise = L - d_acc - d_brk
assert d_cruise > 0
while True:
    if phase == 'brake' and v <= 0.5 and a == 0.0:
        break
    if phase == "accel":
        if x >= d_acc: phase = "cruise"; a = 0.0
        else:
            # trapezoidal accel with jerk ramps
            if v < A*tj/2: a = min(A, a + J*dt)
            elif VC - v < A*tj/2 + 1e-9: a = max(0.0, a - J*dt)
            else: a = A
    elif phase == "cruise":
        a = 0.0
        if x >= d_acc + d_cruise: phase = "brake"
    else:
        if v <= 0.5: a = 0.0; v = 0.0
        elif v < AE*tj/2: a = max(-AE, a + J*dt)
        else: a = -AE
    Fd = drag_force(v, RHO, CD, AF)
    Fp = M*a + Fd
    if Fp >= 0:
        Pp = Fp*v/ETA/1000.0; E_prop += Pp*dt
    else:
        Pp = Fp*v*REGEN/1000.0; E_regen += -Pp*dt
    E_lev += P_LEV*dt; E_aux += P_AUX*dt
    rows.append((t, x/1000, v*3.6, a, Pp, P_LEV, P_AUX,
                 (E_prop - E_regen + E_lev + E_aux)/3600))
    v += a*dt; v = max(v, 0.0)
    x += v*dt; t += dt

rows = np.array(rows)
fig, ax = plt.subplots(4, 1, figsize=(9, 11), sharex=True)
ax[0].plot(rows[:,0]/60, rows[:,2]); ax[0].set_ylabel("speed [km/h]")
ax[1].plot(rows[:,0]/60, rows[:,1]); ax[1].set_ylabel("distance [km]")
ax[2].plot(rows[:,0]/60, rows[:,4], label="traction (+draw)")
ax[2].plot(rows[:,0]/60, rows[:,5], label="levitation")
ax[2].plot(rows[:,0]/60, rows[:,6], label="aux/medical")
ax[2].set_ylabel("power [kW]"); ax[2].legend(loc="upper right", fontsize=8)
ax[3].plot(rows[:,0]/60, rows[:,7]); ax[3].set_ylabel("net energy [kWh]")
ax[3].set_xlabel("time [min]")
for a_ in ax: a_.grid(alpha=0.3)
fig.suptitle("EXP-1 Simulated Delhi-Mumbai run: 1450 km, 1165 km/h cruise, 100 Pa tube, 750 kg pod\n"
             "MODEL OUTPUT - simulation, not physical test data", fontsize=10)
fig.tight_layout()
fig.savefig("../plots/fig_e1_route_trajectory.png", dpi=160)
summary = dict(
  t_total_min = round(t/60, 1), t_accel_min = None,
  d_accel_km = round(d_acc/1000, 1), d_cruise_km = round(d_cruise/1000, 1),
  d_brake_km = round(d_brk/1000, 1),
  E_traction_kWh = round(E_prop/3600, 1), E_regen_kWh = round(E_regen/3600, 1),
  E_lev_kWh = round(E_lev/3600, 1), E_aux_kWh = round(E_aux/3600, 1),
  E_net_kWh = round((E_prop - E_regen + E_lev + E_aux)/3600, 1),
  peak_power_kW = round(rows[:,4].max(), 1))
json.dump(summary, open("../results/exp1_summary.json", "w"), indent=1)
with open("../results/exp1_timeseries.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["t_s","x_km","v_kmh","a_ms2","P_traction_kW","P_lev_kW","P_aux_kW","E_net_kWh"])
    w.writerows(rows[::20])
print(json.dumps(summary, indent=1))
