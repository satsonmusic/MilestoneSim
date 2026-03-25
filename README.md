# 📈 MilestoneSim - Monte Carlo Schedule Engine

> **Predictive Program Intelligence.** A probabilistic forecasting engine designed to model the uncertainty of complex hardware and software delivery timelines.

In high-stakes engineering, "single-point" delivery dates are often unrealistic. **MilestoneSim** uses Monte Carlo methods and Directed Acyclic Graph (DAG) modeling to provide a range of probable outcomes. By running thousands of simulations based on min/max/likely task durations, it identifies the "P80 Confidence" date and highlights the specific critical-path drivers that dominate schedule variance.

## 🚀 Key Features

* **Probabilistic Forecasting:** Calculates P50 (Median), P80 (Confidence), and P90 (Conservative) delivery distributions.
* **DAG Dependency Mapping:** Implements Kahn’s Algorithm to topologically sort complex task relationships and ensure a valid critical path.
* **Sensitivity Analysis:** Programmatically identifies "Risk Drivers"—the tasks most likely to be on the critical path across 5,000+ simulations.
* **Zero-Dependency Core:** Built using pure Python 3.12 (Standard Library) for maximum portability and high-performance simulation.

## 🛠️ Tech Stack

* **Language:** Python 3.12 (Standard Library)
* **Logic:** Monte Carlo Simulation, Kahn’s Algorithm, Triangular Distribution
* **Analysis:** Statistical Confidence Intervals & Critical Path Frequency

## ⚙️ How to Run

### 1. Clone the Repository
```bash
git clone [https://github.com/satsonmusic/MilestoneSim.git](https://github.com/satsonmusic/MilestoneSim.git)
cd MilestoneSim
