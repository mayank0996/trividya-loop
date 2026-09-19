"""EXP-5: Radiative heat rejection from pod in evacuated tube.
MODEL OUTPUT - simulated."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, csv
from model import radiative_W
Ts = np.linspace(295, 335, 200)   # skin temp [K]
fig, ax = plt.subplots(figsize=(8.5, 5))
with open("../results/exp5_thermal.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["skin_K","skin_C","Q_rad_W@A10","Q_rad_W@A15","Q_rad_W@A20"])
    for i in range(0, 200, 10):
        w.writerow([round(Ts[i],1), round(Ts[i]-273.15,1)] + [round(radiative_W(Ts[i],300.0,0.85,A),1) for A in (10,15,20)])
for A, c in zip((10, 15, 20), ("#F58518","#4C78A8","#54A24B")):
    ax.plot(Ts-273.15, [radiative_W(t, 300.0, 0.85, A) for t in Ts], label=f"surface {A} m2", color=c)
for q, ls in ((1000, "--"), (2000, "-."), (3000, ":")):
    ax.axhline(q, color="gray", ls=ls, lw=1); ax.text(21.5, q+40, f"internal load {q/1000:.0f} kW", fontsize=8, color="gray")
ax.axvline(40, color="k", ls="--", lw=1); ax.text(40.3, 250, "skin limit 40 C", fontsize=8)
ax.set_xlabel("pod skin temperature [degC] (tube wall 27 degC, emissivity 0.85)")
ax.set_ylabel("radiative heat rejection [W]")
ax.grid(alpha=0.3); ax.legend(fontsize=8)
ax.set_title("EXP-5 Only radiation rejects heat in a near-vacuum tube\nMODEL OUTPUT - simulation, not physical test data", fontsize=10)
fig.tight_layout(); fig.savefig("../plots/fig_e5_thermal.png", dpi=160)
q = radiative_W(313.15, 300.0, 0.85, 15.0)
print("Q_rad at 40C skin, 15 m2:", round(q,0), "W  -> max safe internal heat load")
