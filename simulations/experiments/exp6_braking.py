"""EXP-6: Emergency stopping distance/time vs speed and deceleration.
MODEL OUTPUT - simulated."""
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, csv
v_kmh = np.linspace(50, 1200, 200)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
with open("../results/exp6_braking.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["v_kmh"] + sum([[f"d_stop_km_ae{a}", f"t_stop_s_ae{a}"] for a in (2,3,5)], []))
    for i in range(0, 200, 5):
        vv = v_kmh[i]; row = [round(vv,1)]
        for a in (2,3,5):
            v = vv/3.6; row += [round(v*v/(2*a)/1000,3), round(v/a,1)]
        w.writerow(row)
for a, c in zip((2,3,5), ("#E45756","#4C78A8","#54A24B")):
    v = v_kmh/3.6
    ax1.plot(v_kmh, v*v/(2*a)/1000, label=f"a_e = {a} m/s2", color=c)
    ax2.plot(v_kmh, v/a, label=f"a_e = {a} m/s2", color=c)
ax1.set_ylabel("emergency stop distance [km]"); ax2.set_ylabel("emergency stop time [s]")
for ax in (ax1, ax2):
    ax.set_xlabel("initial speed [km/h]"); ax.grid(alpha=0.3); ax.legend(fontsize=8)
    ax.axvline(1165, color="k", ls=":", lw=1)
fig.suptitle("EXP-6 Emergency braking envelope (contactless braking assumed available)\nMODEL OUTPUT - simulation, not physical test data", fontsize=10)
fig.tight_layout(); fig.savefig("../plots/fig_e6_braking.png", dpi=160)
for vv in (200, 600, 1165):
    v = vv/3.6
    print(vv, "km/h @3 m/s2: stop", round(v*v/(2*3)/1000,2), "km,", round(v/3,1), "s; @5:", round(v*v/(2*5)/1000,2), "km")
