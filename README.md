# Trividya-Loop

**A student engineering concept for high-speed emergency patient transport.**

> [!IMPORTANT]
> Trividya-Loop is supported by a person-scale pod mockup, 2D engineering drawings, baseline 3D models and exploratory calculations. It is **not** an operational Hyperloop, vacuum transport, levitation or clinical system. Simulation outputs are assumption-driven and are not physical validation.

## Project at a glance

| Category | Current evidence |
| --- | --- |
| Demonstrated | Person-scale pod mockup; 2D drawing set; baseline OBJ/STL models; documented system architecture |
| Modeled | Route timing, drag/pressure, energy, throughput, thermal and braking scenarios |
| Proposed | Low-pressure guideway, propulsion/levitation, emergency workflow, sensing and communications |
| Not validated | Full-scale transport, vacuum operation, levitation, clinical safety, regulatory compliance or real-world performance |


## Why it exists

Emergency transfers lose time at the boundaries between ambulances, hospitals and transport networks. Trividya-Loop explores what a purpose-built patient pod and controlled guideway might require at system level: patient access, equipment layout, routing, sensing, communications, evacuation, thermal management and safe stopping.

This repository focuses on making those requirements and assumptions inspectable. It does not present the concept as a finished transport system.

## Repository map

- [`drawings/`](drawings/) - reviewed 2D engineering drawing set
- [`models/`](models/) - baseline OBJ/STL/MTL models, dimensions and preview renders
- [`simulation/`](simulation/) - exploratory Python models and derived figures
- [`docs/evidence-register.md`](docs/evidence-register.md) - what each artifact supports
- [`docs/system-boundary.md`](docs/system-boundary.md) - what is outside the demonstrated system
- [`docs/assumptions.md`](docs/assumptions.md) - modeling assumptions and limits
- [`docs/ai-assistance.md`](docs/ai-assistance.md) - authorship and tool disclosure

## Evidence boundary

The public artifacts establish design activity, a physical mockup and reproducible exploratory modeling. They do not establish novelty, medical efficacy, infrastructure feasibility, certified safety or commercial readiness. Claims such as "world's first" are intentionally excluded.

## Next validation steps

1. Freeze a traceable requirements matrix.
2. Build a benchtop guideway and instrument braking repeatability.
3. Measure pod mass, power, thermal load and sensor performance.
4. Run evacuation and loss-of-power failure-mode reviews.
5. Seek independent review from transport, control and medical-device specialists.

## Authorship and AI assistance

The project concept, historical mockup and personal evidence are Mayank Kasana's. AI tools assisted with documentation structure, code cleanup, diagrams and editorial review. Reconstructed or AI-assisted artifacts are labeled and are not presented as contemporaneous proof of the original build.

## Links

[Portfolio](https://imayankkasna.lovable.app/) · [LinkedIn](https://www.linkedin.com/in/mayank-kasana-00229b306) · [Profile](https://github.com/mayank0996)

## Rights

No license is granted by default. See [`LICENSES.md`](LICENSES.md) for artifact-level rights and provenance before reuse.
