"""EXP-3: Per-trip energy breakdown across mass x speed scenarios.
MODEL OUTPUT - simulated."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, csv, json
from model import rho_air, drag_force, trip_profile

L = 1450e3
RHO = rho_air(100.0, 300.0)
CD, AF, ETA, REGEN = 0.3, 1.327, 0.90, 0.60
ACCEL = 1.0
scenarios = [(m, s) for m in (400, 750, 1500) for s in (200, 600, 1165)]
labels, parts = [], []
with open("../results/exp3_energy.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["mass_kg","cruise_kmh","t_total_min","KE_net_kWh","drag_kWh","lev_kWh","aux_kWh","motor_loss_kWh","total_kWh","Wh_per_tkm"])
    for m, s in scenarios:
        v = s/3.6
        prof = trip_profile(L, v, ACCEL, 0.5)
        t_tot = prof["t_total"]
        # kinetic: input through motor efficiency, recover regen fraction of raw KE
        ke_in = 0.5*m*v*v / ETA
        ke_regen = REGEN * 0.5*m*v*v
        # drag work over route (approx: v-profile weighted; use cruise drag * L)
        Fd = drag_force(v, RHO, CD, AF)
        drag_E = Fd * L / ETA
        lev = 1.0*(m/1000)*t_tot*1000      # J
        aux = 1000.0*t_tot
        total_J = (ke_in - ke_regen) + drag_E + lev + aux
        conv = 1/3.6e6
        row = dict(mass_kg=m, cruise_kmh=s, t_total_min=round(t_tot/60,1),
                   KE_net_kWh=round((ke_in-ke_regen)*conv,1), drag_kWh=round(drag_E*conv,1),
                   lev_kWh=round(lev*conv,1), aux_kWh=round(aux*conv,1),
                   motor_loss_kWh=round((ke_in-0.5*m*v*v + drag_E*(1-ETA)/ETA)*conv,1),
                   total_kWh=round(total_J*conv,1),
                   Wh_per_tkm=round(total_J/3600/((m/1000)*(L/1000)),1))
        w.writerow(list(row.values()))
        labels.append(f"{m} kg / {s} km/h")
        parts.append((row["KE_net_kWh"], row["drag_kWh"], row["lev_kWh"], row["aux_kWh"], row["total_kWh"], row["Wh_per_tkm"]))
parts = np.array(parts)
x = np.arange(len(labels))
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
bot = np.zeros(len(labels))
for i, (name, c) in enumerate([("net kinetic", "#4C78A8"), ("aero drag", "#F58518"),
                               ("levitation", "#54A24B"), ("aux/medical", "#B279A2")]):
    ax1.bar(x, parts[:, i], bottom=bot, label=name, color=c); bot += parts[:, i]
ax1.set_xticks(x); ax1.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
ax1.set_ylabel("energy per one-way trip [kWh]"); ax1.legend(fontsize=8); ax1.grid(alpha=0.3, axis="y")
ax2.bar(x, parts[:, 5], color="#4C78A8")
ax2.set_xticks(x); ax2.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
ax2.set_ylabel("specific energy [Wh/tonne-km]"); ax2.grid(alpha=0.3, axis="y")
fig.suptitle("EXP-3 Simulated energy per 1450 km one-way trip, 100 Pa tube\nMODEL OUTPUT - simulation, not physical test data", fontsize=10)
fig.tight_layout(); fig.savefig("../plots/fig_e3_energy.png", dpi=160)
print(open("../results/exp3_energy.csv").read())
