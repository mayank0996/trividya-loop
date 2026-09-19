"""EXP-7: Sensitivity (tornado) of trip time and net trip energy to parameter bounds.
MODEL OUTPUT - simulated."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
from model import rho_air, drag_force, trip_profile

def run(L=1450e3, m=750, s=1165, Cd=0.3, P=100.0, a=1.0, eta=0.90, regen=0.60,
        lev_kWt=1.0, aux_kW=1.0):
    v = s/3.6
    prof = trip_profile(L, v, a, 0.5)
    t = prof["t_total"]
    rho = rho_air(P, 300.0)
    Fd = drag_force(v, rho, Cd, 1.327)
    ke_in = 0.5*m*v*v/eta; ke_re = regen*0.5*m*v*v
    dragE = Fd*L/eta
    E = (ke_in-ke_re+dragE+lev_kWt*(m/1000)*t*1000+aux_kW*1000*t)/3.6e6
    return t/60, E

base_t, base_E = run()
params = [
 ("route length 1150/1450 km",      dict(L=1150e3), dict(L=1450e3)),
 ("mass 400/1500 kg",               dict(m=400), dict(m=1500)),
 ("cruise 200/1165 km/h",           dict(s=200), dict(s=1165)),
 ("Cd 0.2/1.0",                     dict(Cd=0.2), dict(Cd=1.0)),
 ("pressure 10/1000 Pa",            dict(P=10.0), dict(P=1000.0)),
 ("accel 0.5/2.0 m/s2",             dict(a=0.5), dict(a=2.0)),
 ("motor eff 0.85/0.95",            dict(eta=0.85), dict(eta=0.95)),
 ("regen 0.4/0.7",                  dict(regen=0.4), dict(regen=0.7)),
 ("lev power 0.5/3.0 kW/t",         dict(lev_kWt=0.5), dict(lev_kWt=3.0)),
 ("aux load 0.5/2.5 kW",            dict(aux_kW=0.5), dict(aux_kW=2.5)),
]
labels, tlo, thi, elo, ehi = [], [], [], [], []
for name, lo, hi in params:
    tl, el = run(**lo); th, eh = run(**hi)
    labels.append(name); tlo.append(tl-base_t); thi.append(th-base_t)
    elo.append(el-base_E); ehi.append(eh-base_E)
order = np.argsort([abs(a)+abs(b) for a, b in zip(elo, ehi)])
labels = [labels[i] for i in order]; tlo=[tlo[i] for i in order]; thi=[thi[i] for i in order]
elo=[elo[i] for i in order]; ehi=[ehi[i] for i in order]
y = np.arange(len(labels))
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), sharey=True)
for i in y:
    ax1.barh(i, thi[i]-tlo[i], left=tlo[i], color="#4C78A8", alpha=0.8)
    ax2.barh(i, ehi[i]-elo[i], left=elo[i], color="#F58518", alpha=0.8)
ax1.axvline(0, color="k", lw=0.8); ax2.axvline(0, color="k", lw=0.8)
ax1.set_yticks(y); ax1.set_yticklabels(labels, fontsize=8)
ax1.set_xlabel(f"delta trip time [min] around base {base_t:.0f} min")
ax2.set_xlabel(f"delta trip energy [kWh] around base {base_E:.0f} kWh")
fig.suptitle("EXP-7 One-at-a-time sensitivity to assumption bounds (baseline v1.0)\nMODEL OUTPUT - simulation, not physical test data", fontsize=10)
fig.tight_layout(); fig.savefig("../plots/fig_e7_sensitivity.png", dpi=160)
json.dump(dict(base_trip_min=round(base_t,1), base_energy_kWh=round(base_E,1)), open("../results/exp7_base.json","w"))
print("base:", round(base_t,1), "min,", round(base_E,1), "kWh")
