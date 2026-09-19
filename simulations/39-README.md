# Assumption-driven simulations

These Python experiments are exploratory calculations, not measured hardware results. Every output inherits the assumed values and open measurement items in `params.py`. They do not validate speed, energy use, braking, thermal behavior, communications, patient safety, clinical performance or infrastructure feasibility.

## Reproduce

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cd experiments
for f in exp*.py; do python "$f"; done
```

Scripts write CSV/JSON to `results/` and plots to `plots/`. Committed outputs are included so reviewers can compare a rerun. Python 3.11 was used for the reviewed release.

`exp8_data_workflow.py` uses synthetic stream categories and assumed bitrates only. It contains no patient records or real medical data.
