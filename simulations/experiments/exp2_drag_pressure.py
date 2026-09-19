"""EXP-2: Aerodynamic drag and cruise power vs speed at several tube pressures.
MODEL OUTPUT - simulated."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, csv
from model import rho_air, drag_force, speed_of_sound

CD, AF = 0.3, 1.327
v = np.linspace(0, 350, 351)             # m/s
pressures = [(10, "10 Pa"), (100, "100 Pa (baseline)"), (1000, "1000 Pa"), (101325, "sea level")]
a_snd = speed_of_sound(300.0)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 8), sharex=True)
with open("../results/exp2_drag.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["v_m_s","v_kmh","mach"] + [f"F_drag_N@{p}Pa" for p, _ in pressures] + [f"P_kW@{p}Pa" for p, _ in pressures])
    for i, vv in enumerate(v):
        Fs = [drag_force(vv, rho_air(p, 300.0), CD, AF) for p, _ in pressures]
        Ps = [F*vv/1000 for F in Fs]
        if i % 10 == 0:
            w.writerow([round(vv,1), round(vv*3.6,1), round(vv/a_snd,3)] + [round(F,2) for F in Fs] + [round(P,2) for P in Ps])
        for (p, lbl), F in zip(pressures, Fs):
            pass
for p, lbl in pressures:
    rho = rho_air(p, 300.0)
    F = np.array([drag_force(vv, rho, CD, AF) for vv in v])
    ax1.plot(v*3.6, F, label=lbl)
    ax2.plot(v*3.6, F*v/1000, label=lbl)
for ax in (ax1, ax2):
    ax.axvline(0.8*a_snd*3.6, color="k", ls="--", lw=1)
    ax.set_yscale("log"); ax.grid(alpha=0.3, which="both"); ax.legend(fontsize=8, loc="upper left")
ax1.set_ylabel("drag force [N]"); ax2.set_ylabel("power to overcome drag [kW]")
ax2.set_xlabel("pod speed [km/h]")
ax1.annotate("Mach 0.8 at 300 K (1000 km/h):\nrecommended cruise cap near transonic", xy=(610, 3000), fontsize=8)
fig.suptitle("EXP-2 Drag vs speed at tube pressures (Cd=0.3, A=1.327 m2, T=300 K)\nMODEL OUTPUT - simulation, not physical test data", fontsize=10)
fig.tight_layout(); fig.savefig("../plots/fig_e2_drag_pressure.png", dpi=160)
print("Mach@1165km/h:", round(1165/3.6/a_snd, 3), "| a_sound =", round(a_snd,1), "m/s")
for p, lbl in pressures:
    F = drag_force(1165/3.6, rho_air(p,300.0), CD, AF)
    print(lbl, "F@1165km/h =", round(F,1), "N, P =", round(F*1165/3.6/1000,1), "kW")
