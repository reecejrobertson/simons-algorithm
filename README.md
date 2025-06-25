# Simon's Algorithm in the NISQ Cloud

This repository contains experimental implementations of Simon's Algorithm on noisy intermediate-scale quantum (NISQ) devices using IBM and IonQ cloud-accessible quantum hardware.
For a detailed discussion of the methods and results, refer to the associated publication:
[Entropy 27, 658 (2025)](https://www.mdpi.com/1099-4300/27/7/658).

## Table of Contents

- [Introduction](#introduction)
- [Structure](#structure)
- [Usage](#usage)
- [License](#license)

## Introduction

Let $\\{0,1\\}^n$ be the set of all binary bitstrings of length $n$.
Suppose that one is given a black-box oracle function $f(x):\\{0,1\\}^n\rightarrow\\{0,1\\}^{n-1}$ with the property that there exists some fixed $s\in\\{0,1\\}^n$ such that $f(x) = f(x')$ for all $x \neq x'$ if and only if $x \oplus x' = s$.
In other words, $f(x)$ is a two-to-one periodic function with period $s$.
Simon's problem is to identify $s$, where the only allowable operation is to query $f$.
Simon showed that a fault-tolerant gate-based quantum computer can solve this problem with exponential advantage over a classical computer (https://epubs.siam.org/doi/10.1137/S0097539796298637).

This repository implements Simon’s algorithm in practice, analyzing its performance on real NISQ devices, including IonQ and IBM hardware.
From the paper abstract,

> Simon’s algorithm was one of the first to demonstrate a genuine quantum advantage in solving a problem. The algorithm, however, assumes access to fault-tolerant qubits. In our work, we use Simon’s algorithm to benchmark the error rates of devices currently available in the "quantum cloud". As a main result, we objectively compare the different physical platforms made available by IBM and IonQ. Our study highlights the importance of understanding the device architectures and topologies when transpiling quantum algorithms onto hardware. For instance, we demonstrate that two-qubit operations on spatially separated qubits on superconducting chips should be avoided.

## Structure

The repository structure is as follows:

```
simons-algorithm/
├── src/                       # Core implementation and analysis code
│   ├── cnotTest.py            # Tests the fidelity of CNOT gates based on qubit distance
│   ├── combinedPlotting.ipynb # Generates publication-quality plots from data
│   ├── dataGeneration.py      # Runs Simon's algorithm on quantum hardware
│   ├── forteGeneration.ipynb  # Collects data from IonQ's Forte device
│   ├── imbDataCollection.py   # Gathers results from IBMQ jobs
│   └── plotting.py            # Utilities for creating plots from experimental data
├── APIs/                      # API folder (must be created locally)
│   ├── IBM_API.txt            # IBM API file (must be created locally)
│   ├── IonQ_API.txt           # IonQ API file (must be created locally)
├── data/                      # Experimental data for Simon's algorithm
├── cnotData/                  # Results of experiments on CNOT fidelity vs. distance
├── figures/                   # Figures generated from data for publication
├── archive/                   # Legacy code, diagrams, and poster materials
├── .gitignore                 # Specifies untracked files to ignore
├── LICENSE                    # Project license
└── README.md                  # This file
```

The most important scripts are located in the ``src/`` directory. These perform data collection, analysis, and visualization, and were used to generate the figures and results in the published paper.

## Usage

To run Simon’s algorithm on NISQ devices and analyze the results:

* Generate Data
  - IonQ: Use dataGeneration.py or forteGeneration.ipynb to submit jobs.
  - IBM: Use the IBM composer tool to submit jobs, and imbDataCollection.py to collect job results.
* CNOT Benchmarking
  - Run cnotTest.py to test how the CNOT error rate varies with qubit separation.
* Plotting and Analysis
  - Use plotting.py, combinedPlotting.ipynb, or forteGeneration.ipynb to visualize the collected data.
  - Figures are saved in the figures/ directory.

Note: Access to IBM or IonQ cloud resources requires API credentials.

## License

This project is licensed under the MIT License — see the LICENSE file for details.
