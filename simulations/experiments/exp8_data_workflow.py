"""EXP-8: Synthetic sensor/data workflow budget for one trip.
MODEL OUTPUT - computed budget, not measured link data."""
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, csv, json
streams = [
 ("12-lead ECG (500 Hz, 16 bit)", 0.096),
 ("SpO2 + pleth waveform", 0.008),
 ("NIBP / capnography / temp", 0.005),
 ("Pod state + location telemetry", 0.032),
 ("Audio channel (compressed)", 0.032),
 ("2x 1080p H.264 video", 4.0),
]
total_mbps = sum(s[1] for s in streams)
t_trip_min = 80.0
gb = total_mbps/8*60*t_trip_min/1000
with open("../results/exp8_data_budget.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["stream","bitrate_Mbps","data_per_80min_trip_MB"])
    for n, b in streams:
        w.writerow([n, b, round(b/8*60*t_trip_min,1)])
    w.writerow(["TOTAL", round(total_mbps,3), round(gb*1000,0)])
t = np.linspace(0, t_trip_min, 100)
fig, ax = plt.subplots(figsize=(8.5, 4.5))
for mode, rate, c in [("full stream (~4.2 Mbps)", total_mbps, "#4C78A8"),
                      ("vital signs + telemetry only (~0.2 Mbps)", 0.173, "#54A24B")]:
    ax.plot(t, rate/8*60*t/1000, label=mode, color=c)
ax.set_xlabel("trip time [min]"); ax.set_ylabel("accumulated data [GB]")
ax.grid(alpha=0.3); ax.legend(fontsize=8)
ax.set_title("EXP-8 Accumulated synthetic telemetry data per trip (store-and-forward + live link)\nMODEL OUTPUT - computed budget, not physical test data", fontsize=10)
fig.tight_layout(); fig.savefig("../plots/fig_e8_data_budget.png", dpi=160)
json.dump(dict(total_mbps=round(total_mbps,3), gb_per_80min=round(gb,2)),
          open("../results/exp8_summary.json","w"), indent=1)
print("total Mbps:", round(total_mbps,3), "| GB per 80-min trip:", round(gb,2))
