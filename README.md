# Teaching Notes Repository

## Dr. Ian Helfrich - Behavioral Economics Interactive Notebooks

This repository contains comprehensive, interactive teaching materials for behavioral economics at the PhD level. The notebooks combine rigorous mathematical treatment with accessible explanations and hands-on simulations.

### Contents

#### 01_comprehensive_behavioral_economics.ipynb
A comprehensive introduction to behavioral economics covering:

- **Prospect Theory**: Mathematical formulation, value function, probability weighting
- **Loss Aversion**: Endowment effect, reference dependence, applications  
- **Mental Accounting**: Fungibility violations, budgeting behaviors
- **Anchoring & Adjustment**: Heuristics and insufficient adjustment
- **Framing Effects**: Gain/loss frames and decision contexts

Each section includes:
- Intuitive explanations with real-world examples
- Mathematical formalization using LaTeX
- Interactive demonstrations with parameter adjustment widgets
- Agent-based simulations showing emergent behaviors
- Connections to recent research and applications

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
