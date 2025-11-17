# Λ‑Möbius Pentastrat AI‑OS Architecture

> **Forma supremă a AI‑OS** — Organism cibernetic pentastrat extins, coordonat de Λ‑Arbiter Core (RL/MPC), care operează pe un ciclu fractal de întreținere și îmbunătățire continuă.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)

## 🌀 Core Principle

**Timpul total de lucru este comprimat prin Λ‑Time Wrap** astfel încât costul dominant rămâne **T₁** (inițiere/detectare), iar câștigurile se acumulează în **k·P** (eficiență × paralelism). Sistemul se auto-repară, auto-optimizează și se stabilizează în bucle fractale controlate.

## 🎯 Key Features

- ✅ **Self-Maintaining**: Detect → Quarantine → Improve → Reinvest cycle
- ✅ **Self-Optimizing**: Adaptive metabolism (quantization, pruning, JIT)
- ✅ **Temporal Compression**: Λ‑Time Wrap for 95% fast-path, 5% slow-path
- ✅ **Hardware ↔ Cloud ↔ Edge**: Intelligent resource allocation
- ✅ **Security First**: Attestation, sandboxing, kill-switch
- ✅ **Observable**: Complete telemetry, tracing, root cause analysis
- ✅ **Economic**: ROI-driven reinvestment and budgeting

## 🏗️ Architecture

### Pentastrat Core Layers

```
┌─────────────────────────────────────────────────────────────┐
│                   Λ‑Arbiter Core (8001)                     │
│            Meta-decisional cortex (RL/MPC)                  │
│     Decides: Wrap/Steady/Unwrap | Allocates: P, Budget     │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐   ┌────────▼────────┐   ┌───────▼────────┐
│  Λ‑Regen (8005)│   │ Λ‑Optimize (8004)│   │Λ‑Balance (8003)│
│  Flux Fractal  │   │   Metabolism     │   │  Homeostasis   │
│ Detect→Improve │   │  k·P maximize    │   │  SLA maintain  │
└────────────────┘   └──────────────────┘   └────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                    ┌─────────▼────────┐
                    │ Λ‑Entropy (8006) │
                    │ Controlled Stress│
                    │  A/B, Chaos, Adv │
                    └──────────────────┘
```

### Extended Modules

- **Λ‑TimeWrap (8002)**: Temporal compression engine
- **Λ‑Memory Graph (8007)**: Unified persistent memory
- **Λ‑Safety Guard (8008)**: Security & governance
- **Λ‑Econ (8009)**: Resource & value engine
- **Λ‑Explain (8080)**: Observability & causality
- **Λ‑Planner (8011)**: Task & trajectory planning
- **Λ‑Secure I/O (8010)**: Input/output security gateway

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)

### Launch the System

```bash
# Clone the repository
git clone https://github.com/manuelstellian-dev/-M-bius-Pentastrat-AI-OS-Architecture.git
cd -M-bius-Pentastrat-AI-OS-Architecture

# Start all services
./tools/scripts/bootstrap.sh

# Or use Docker Compose directly
docker-compose up -d
```

### Access the Services

- **Grafana Dashboard**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Λ‑Arbiter Core**: http://localhost:8001
- **Λ‑TimeWrap**: http://localhost:8002
- **All services**: See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for complete list

### Test the System

```bash
# Test Arbiter decision making
curl -X POST http://localhost:8001/decide_mode \
  -H 'Content-Type: application/json' \
  -d '{"theta": 0.82}'

# Test TimeWrap temporal compression
curl -X POST http://localhost:8002/lambda_time \
  -H 'Content-Type: application/json' \
  -d '{"mode":1,"T1":10,"k":2,"P":1.2,"U":8}'

# Test Balance PID control
curl -X POST http://localhost:8003/tune \
  -H 'Content-Type: application/json' \
  -d '{"lat_p99":95.5,"Lmax":100.0}'
```

## 📊 Λ‑Time Formulas

### Wrap Mode (Compression, Θ ≥ θ_high)
```
Λ = T₁·log(U) / (1 - 1/(k·P))
Condition: k·P > 1 + ε
Effect: Compresses time, increases throughput
```

### Steady Mode (Equilibrium, θ_low ≤ Θ < θ_high)
```
Λ = T₁·log(U)
Effect: Maintains temporal scale
```

### Unwrap Mode (Expansion, Θ < θ_low)
```
Λ = T₁·log(U) / (1 - k·P)  if |k·P| < 1 - ε
Effect: Expands time for debugging
```

## 🔧 Key Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **T₁** | Initial cost (detect/boot) | Minimize |
| **k** | Efficiency rate per iteration | Maximize |
| **P** | Effective parallelism | Optimize |
| **U** | Utility (scale) | Maximize |
| **Θ** | Resilience composite | 0.55-1.0 |
| **k·P** | Combined efficiency | >1 for Wrap mode |
| **p99** | Tail latency | <120ms (MVP) |
| **MTTR** | Mean time to repair | <10 min |

## 🛡️ Security & Governance

- **Attestation Chain**: Boot-to-cloud verification with TPM/TEE support
- **Dual Authorization**: Arbiter + Safety Guard for system changes
- **Sandboxing**: Isolated execution environment for all changes
- **Change Cards**: Complete audit trail for every modification
- **Kill-Switch**: Emergency stop with superior privilege

## 🌍 Deployment Topology

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Local     │────▶│    Cloud     │◀────│     Edge     │
│  (Hardware)  │     │  (Training)  │     │(Distillation)│
├──────────────┤     ├──────────────┤     ├──────────────┤
│ Low latency  │     │ Heavy compute│     │ Personalized │
│ Quarantine   │     │ Aggregation  │     │ Federated    │
│ FPGA/uCode   │     │ Planning     │     │ Rollback     │
└──────────────┘     └──────────────┘     └──────────────┘
```

## 📖 Documentation

- [Complete Architecture](docs/ARCHITECTURE.md) - Detailed system design
- [API Reference](docs/API.md) - Endpoint documentation (TODO)
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment (TODO)
- [Runbooks](docs/runbooks/) - Operational procedures (TODO)

## 🔬 Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run a single service
cd services/arbiter
python main.py

# Run tests
pytest tests/
```

### Project Structure

```
.
├── services/           # All microservices
│   ├── arbiter/       # Λ‑Arbiter Core
│   ├── timewrap/      # Λ‑TimeWrap
│   ├── balance/       # Λ‑Balance
│   ├── optimize/      # Λ‑Optimize
│   ├── regen/         # Λ‑Regen
│   ├── entropy/       # Λ‑Entropy
│   ├── memory/        # Λ‑Memory Graph
│   ├── safety/        # Λ‑Safety Guard
│   ├── econ/          # Λ‑Econ
│   ├── explain/       # Λ‑Explain
│   ├── planner/       # Λ‑Planner
│   └── secureio/      # Λ‑Secure I/O
├── infra/             # Infrastructure configs
│   ├── k8s/          # Kubernetes manifests
│   ├── opa/          # Policy definitions
│   └── prometheus/   # Monitoring config
├── tools/             # Scripts and utilities
├── docs/              # Documentation
└── tests/             # Test suites
```

## 🎓 Theoretical Foundation

### Flux Fractal Cycle
```
PREDICT → DETECT → ANALYZE → QUARANTINE → NEUTRALIZE 
    ↓         ↓         ↓           ↓            ↓
→ VALIDATE → IMPROVE → REINVEST → MONITOR → PREDICT
```

Each phase recursively contains the entire cycle, creating a **fractal self-improvement system**.

### Utility Function
```
U = w₁·Throughput + w₂·EnergyEff − w₃·Latency − w₄·Risk − w₅·Cost
```

### Resilience (Θ)
```
Θ = α₁·(1−Lat_p99/Lmax) + α₂·MTBF/(MTBF+MTTR) + α₃·SecScore + α₄·DriftStability
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) (TODO) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by biological homeostasis and economic reinvestment principles
- Built on modern microservices and observability patterns
- Designed for hardware-cloud-edge hybrid architectures

## 📞 Contact

For questions and support, please open an issue on GitHub.

---

**Built with** 🧠 **by the Λ‑Möbius team**

*"The supreme form of AI‑OS — self-maintaining, self-optimizing, and infinitely scalable"*
