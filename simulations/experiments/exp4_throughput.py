"""EXP-4: Line throughput vs cruise speed and emergency deceleration.
Headway = emergency stop time + margin. MODEL OUTPUT - simulated."""
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, csv
v_kmh = np.linspace(100, 1200, 200)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
with open("../results/exp4_throughput.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["v_kmh"] + [f"tph_ae{a}" for a in (2,3,5)])
    for vv in v_kmh:
        row = [round(vv,1)]
        for ae in (2,3,5):
            v = vv/3.6
            headway = v/ae + 20.0
            row.append(round(3600/headway,1))
        w.writerow(row)
for ae, c in zip((2,3,5), ("#E45756","#4C78A8","#54A24B")):
    v = v_kmh/3.6
    hw = v/ae + 20.0
    ax1.plot(v_kmh, hw, label=f"a_e = {ae} m/s2", color=c)
    ax2.plot(v_kmh, 3600/hw, label=f"a_e = {ae} m/s2", color=c)
for ax, yl in ((ax1, "minimum safe headway [s]"), (ax2, "throughput [pods/hour/direction]")):
    ax.set_xlabel("cruise speed [km/h]"); ax.set_ylabel(yl); ax.grid(alpha=0.3); ax.legend(fontsize=8)
    ax.axvline(1165, color="k", ls=":", lw=1)
ax2.annotate("1 patient/pod ->\npatients/h = pods/h", xy=(600, 60), fontsize=8)
fig.suptitle("EXP-4 Throughput limited by emergency stopping (margin 20 s)\nMODEL OUTPUT - simulation, not physical test data", fontsize=10)
fig.tight_layout(); fig.savefig("../plots/fig_e4_throughput.png", dpi=160)
for vv in (200, 600, 1165):
    v = vv/3.6
    print(vv, "km/h: headway", round(v/3+20,1), "s ->", round(3600/(v/3+20),1), "pods/h | stop dist", round(v*v/(2*3)/1000,2), "km")
