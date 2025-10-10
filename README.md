
# Curved Dynamic Geometry of Meaning (CDG)

A formal mathematical framework for modeling cognition and consciousness through differential geometry.

## 🎯 Overview

The CDG framework models cognitive processes as dynamics on a meaning-space manifold, transforming the "hard problem" of consciousness from a metaphysical mystery into a geometric phenomenon open to empirical validation.

**Core Insight**: Consciousness emerges as a geometric necessity from sufficiently complex meaning-space dynamics, just as area emerges necessarily from length × width in Cartesian coordinates.

## 🚀 Quick Start

### For Researchers & Scientists
```bash
git clone https://github.com/preciousadeniyi/CDG-Framework.git
cd CDG-Framework/simulations
pip install -r requirements.txt
python minimal_cdg.py
```

### For Developers & AI Researchers
```python
from simulations.minimal_cdg import MinimalCDG
cdg = MinimalCDG()
trajectory = cdg.simulate_thought_trajectory('sadness', 'joy')
```

### For Clinicians & Therapists
See [Clinical Applications](sections/05-applications.md#54-psychopathology-as-geometric-distortion) for geometric signatures of mental health conditions.

### For Philosophers & General Readers
Start with the [Non-Technical Summary](sections/15-non-technical.md) and [Visual Diagrams](sections/12-diagrams.md).

## 🆕 Beginner Setup Guide

If you're new to GitHub, Python, or running code like this, follow these steps to get everything working smoothly. This should take 10-15 minutes.

### Prerequisites
- **Python**: Version 3.10 or higher (download from https://www.python.org if needed).
- **Git**: For cloning the repository (install from https://git-scm.com if you don't have it).
- **Operating System**: Works on Windows, macOS, or Linux. If on Windows, use Command Prompt or PowerShell.
- **Hardware**: Basic computer; no GPU required for simulations.
- **Internet**: Needed initially for cloning and installing dependencies.

### Step-by-Step Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/preciousadeniyi/CDG-Framework.git
   cd CDG-Framework
   ```
   (This downloads all files to your computer.)

2. **Set Up a Virtual Environment** (Recommended to avoid conflicts):
   ```bash
   python -m venv cdg-env
   ```
   - On macOS/Linux: `source cdg-env/bin/activate`
   - On Windows: `cdg-env\Scripts\activate`
   (You'll see `(cdg-env)` in your terminal prompt.)

3. **Install Dependencies**:
   ```bash
   cd simulations
   pip install -r requirements.txt
   ```
   (This installs libraries like numpy, scipy, and matplotlib for simulations.)

4. **Run a Simple Test**:
   ```bash
   python minimal_cdg.py
   ```
   - **What to Expect**: Console output showing a simulated thought trajectory (e.g., from 'sadness' to 'joy') with possible plots or metrics like curvature values. If plots appear, you'll see graphs; otherwise, text results.
   - If successful, try `python run_all.py` to run all demos.

### Common Troubleshooting
- **Python not found**: Ensure Python is in your system's PATH (restart terminal after install).
- **Dependency errors**: Try `pip install --upgrade pip` first, or check for Python version mismatches.
- **No plots show**: Ensure matplotlib is installed; run in an interactive shell if needed.
- **Permission issues**: On macOS/Linux, use `sudo` for pip if required (but virtualenv avoids this).
- Stuck? Check the [Issues](https://github.com/preciousadeniyi/CDG-Framework/issues) tab or ask in discussions.

Once set up, explore the simulations—they demonstrate concepts like emotion dynamics without needing deep math knowledge.

## 📚 Paper Structure

| Section | Description |
|---------|-------------|
| [Abstract](sections/01-abstract.md) | Framework overview and key contributions |
| [Introduction](sections/02-introduction.md) | Problem statement and CDG approach |
| [Mathematical Foundations](sections/03-mathematical-foundations.md) | Differential geometry basis |
| [CDG Framework](sections/04-cdg-framework.md) | Six core principles |
| [Applications](sections/05-applications.md) | Cognitive phenomena explained |
| [Testable Predictions](sections/06-predictions.md) | Empirical validation roadmap |
| [Open Problems](sections/14-open-problems.md) | Research challenges |

## 🔬 Live Simulations

```bash
# Run all demonstrations
cd simulations
python run_all.py

# Or run individual simulations
python minimal_cdg.py
python depression_basin.py
```

**Available Simulations**:
- `minimal_cdg.py` - Basic emotion space dynamics (great for beginners to see simple outputs).
- `depression_basin.py` - Therapeutic curvature smoothing  
- `insight_simulation.py` - Geodesic formation during insight

## 🎨 Visual Guide

- [**Diagrams & Intuitions**](sections/12-diagrams.md) - Conceptual illustrations
- [**Geometric Signatures**](sections/05-applications.md#54-psychopathology-as-geometric-distortion) - Clinical patterns
- [**Mathematical Visualizations**](sections/12-diagrams.md#122-mathematical-visualization) - Core concepts

## 📊 Framework Status

| Component | Status | Version |
|-----------|--------|---------|
| Theoretical Foundation | ✅ Complete | v1.0 |
| Mathematical Formalism | ✅ Complete | v1.0 |
| Empirical Predictions | ✅ Complete | v1.0 |
| Simulation Code | 🟡 Beta | v0.8 |
| Clinical Applications | 🟡 Development | v0.5 |
| AI Implementation | 🟡 Research | v0.3 |

## 🎯 Key Features

### Mathematical Rigor
- Differential geometry foundation
- Riemannian manifold structure
- Curvature-based consciousness threshold

### Testable Predictions
- Neural curvature correlations (ρ > 0.6)
- Reaction time-geodesic relationships (R² > 0.4)
- Clinical curvature reduction (ΔR > 30%)

### Practical Applications
- Geometric psychopathology diagnosis
- AI consciousness benchmarks
- Therapeutic intervention protocols

## 🤝 Contributing

We welcome contributions from:
- **Mathematicians** - Formalization and proofs
- **Neuroscientists** - Experimental validation
- **Clinicians** - Application development
- **AI Researchers** - Implementation
- **Philosophers** - Conceptual analysis

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📫 Citation

```bibtex
@article{cdg2024,
  title={The Curved Dynamic Geometry of Meaning: A Formal Framework for Modeling Cognition and Consciousness},
  author={CDG Research Collective},
  year={2024},
  url={https://github.com/preciousadeniyi/CDG-Framework}
}
```

## 🔗 Quick Links

- [**Full Paper**](index.md) - Complete integrated document
- [**Non-Technical Summary**](sections/15-non-technical.md) - Accessible overview
- [**Glossary**](sections/16-glossary.md) - Key terms explained
- [**Open Problems**](sections/14-open-problems.md) - Research opportunities

## 📄 License

This work is licensed under the MIT License - see [LICENSE](LICENSE) for details.



> **The Cartesian Shift**: Just as Descartes revealed area as length × width, CDG reveals consciousness as geometric necessity.


