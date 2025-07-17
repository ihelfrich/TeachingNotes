# Teaching Notes Repository

## Dr. Ian Helfrich - Behavioral Economics Interactive Notebooks

This repository contains comprehensive, interactive teaching materials for behavioral economics at the PhD level. The notebooks combine rigorous mathematical treatment with accessible explanations and hands-on simulations.

### Contents

#### 01_comprehensive_behavioral_economics.ipynb
A radically enhanced comprehensive behavioral economics notebook covering 12 major topics:

1. **Foundations: Prospect Theory and the Value Function** - Mathematical formulation, empirical evidence, applications
2. **Loss Aversion: Why Losses Loom Larger Than Gains** - Endowment effect, reference dependence, WTA/WTP gaps
3. **Probability Weighting: How We Distort Uncertainty** - Overweighting small probabilities, certainty effect
4. **Mental Accounting: The Psychology of Money** - Fungibility violations, budgeting behaviors, sunk costs
5. **Anchoring and Adjustment: The Power of First Impressions** - Heuristics, insufficient adjustment, applications
6. **Framing Effects: How Context Shapes Decisions** - Gain/loss frames, decision contexts, Asian Disease Problem
7. **Time Preferences: Present Bias and Hyperbolic Discounting** - Exponential vs. hyperbolic models, self-control
8. **Social Preferences: Fairness, Reciprocity, and Altruism** - Ultimatum games, trust games, public goods
9. **Nudges and Choice Architecture: Designing Better Decisions** - Default options, choice overload, libertarian paternalism
10. **Market Anomalies: When Behavioral Biases Meet Finance** - Disposition effect, momentum, value premium
11. **Neuroeconomics: The Brain on Economics** - Neural correlates, dual-process theory, brain imaging studies
12. **Policy Applications: Behavioral Insights in Government** - Nudge units, tax compliance, retirement savings

Each section includes:
- Extensive research citations from leading behavioral economists (Kahneman, Tversky, Thaler, Ariely, Camerer, Fehr, Laibson, DellaVigna, Mullainathan, Shafir)
- Mathematical formalization using LaTeX with proper notation
- Advanced interactive demonstrations with parameter adjustment widgets
- Agent-based simulations showing emergent market behaviors
- Real-world policy applications and empirical findings
- Connections to recent research and experimental evidence

### Features

- **Interactive Widgets**: Adjust parameters in real-time to see how behavioral biases affect decision-making
- **Agent-Based Simulations**: Watch markets populated with behavioral agents evolve over time
- **Mathematical Rigor**: Proper LaTeX formatting for all equations and formal definitions
- **Accessible Style**: Complex concepts explained clearly without sacrificing depth

### Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start Jupyter:
   ```bash
   jupyter notebook
   ```

3. Open `behavioral_economics/notebooks/01_comprehensive_behavioral_economics.ipynb`

### Repository Structure

```
behavioral_economics/
├── notebooks/
│   └── 01_comprehensive_behavioral_economics.ipynb
├── utils/
│   └── economic_functions.py
├── simulations/
│   ├── prospect_theory_agents.py
│   └── market_simulation.py
└── data/
    └── (simulation outputs)
```

### Technical Requirements

- Python 3.8+
- Jupyter Notebook or JupyterLab
- See `requirements.txt` for complete dependency list

### Author

Dr. Ian Helfrich  
School of Economics  
Georgia Institute of Technology

### License

Educational use permitted. Please cite appropriately when using these materials.
