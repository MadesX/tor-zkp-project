# Tor-ZKP: Anonymous and Authenticated Tor Exit Nodes using FFS Zero-Knowledge Proofs

## Overview

This project extends the Tor network with an authentication mechanism based on the Feige–Fiat–Shamir (FFS) Zero-Knowledge Proof protocol.

The implementation is based on the research paper:

“Handling Exit Node Vulnerability in Onion Routing with a Zero-Knowledge Proof”
by Nadav Voloch and Maor Meir Hajaj.

The goal is to preserve user anonymity while allowing Tor exit nodes to prove legitimacy to a trusted verifier without revealing any secret information.

The project implements and evaluates a ZKP-enhanced Tor architecture using:

* modified Tor source code
* Chutney simulation
* authenticated exit-node validation
* Shadow network simulation
* large-scale traffic experiments
* adversarial attack simulations

---

# Main Features

* Multi-round FFS Zero-Knowledge authentication
* Authenticated Tor exit nodes
* External verifier service
* Shadow-based Tor network simulation
* Performance comparison:

  * Standard Tor
  * ZKP-Enhanced Tor
* Medium-scale Tor network experiments
* Throughput and latency evaluation

---

# System Architecture

The system contains:

* Tor Clients
* Tor Relays
* Authenticated Exit Nodes
* External ZKP Verifier
* Shadow simulation environment
* Chutney simulation

Authentication flow:

1. Exit node connects to verifier
2. FFS-ZKP challenge-response protocol executes
3. Verifier validates mathematical proof
4. Exit node becomes trusted
5. Traffic forwarding begins

---

# Technologies Used

* Tor 0.4.8.13
* C
* Python
* Chutney
* Shadow Simulator
* TGen traffic generator
* Ubuntu Linux
* TCP Sockets
* Cryptographic Zero-Knowledge Proofs
* Jupyter notebooks for statistical analysis and benchmarking

---

# Repository Structure

```text
tor_project/
│
├── tor/                     # Modified Tor source code
├── chutney/                 # Chutney simulator
├── shadow/                  # Shadow simulator
├── verifier/                # Python verifier
├── examples/
│   └── docs/
│       └── tor-zkp-comparison/
│           ├── standard/    # Standard Tor experiments
│           └── zkp/         # ZKP-enhanced Tor experiments
│
.
.
.
└── README.md
```

---

# Running the Project

## Activate Environment

```bash
source tor_env/bin/activate
```

## Run Standard Tor Experiment

```bash
cd shadow/examples/docs/tor-zkp-comparison/standard
./run.sh
```

## Run ZKP Tor Experiment

```bash
cd shadow/examples/docs/tor-zkp-comparison/zkp
./run.sh
```

---

# 

## Experimental Result Notebooks

The repository contains multiple Jupyter notebooks used for statistical analysis and benchmarking.

### 1. Large-Scale ZKP-Tor Simulation

```text id="pl2fzd"
zkp_stats_large.ipynb
```

Simulated architecture:

* Clients: 201
* Relays: 20
* Exit Nodes: 4
* Verifier Nodes: 1
* Circuits per Tor Client: 50
* Total Circuits: 10,000

Contains:

* runtime analysis
* throughput measurements
* authentication statistics
* network behavior evaluation

---

### 2. Medium-Scale ZKP-Tor Simulation

```text id="lbz4so"
zkp_stats_testB.ipynb
```

Same architecture with approximately 1,000 circuits for medium-scale evaluation.

---

### 3. Benchmark Comparison

```text id="ob1xez"
zkp_stats_benchmarks.ipynb
```

Contains comparative evaluation between:

* Standard Tor
* ZKP-Enhanced Tor

Measured metrics:

* Runtime
* Circuit success rate

# Security Evaluation

The project includes simulated attack scenarios to evaluate the robustness of the ZKP-authenticated Tor architecture.

Tested attack models include:

* Malicious Exit Node Sabotage
* Packet Modification / Bit-Flip Attacks
* Replay Attacks
* Traffic Snooping Attempts

Each attack scenario was evaluated using dedicated Jupyter notebooks containing:

* simulation outputs
* authentication statistics
* circuit success/failure analysis
* security observations

Security evaluation notebooks:

```text id="lajv8k"
zkp_stats_malicious_exit.ipynb
zkp_stats_bitflip.ipynb
zkp_stats_replay.ipynb
zkp_stats_snooping.ipynb
```

The results demonstrate that authenticated exit verification significantly improves resistance against unauthorized or malicious exit-node behavior.

# Performance Evaluation

The project evaluates and compares the performance of:

* Standard Tor
* ZKP-Enhanced Tor

The comparison focuses on computational overhead and resource utilization during large-scale Shadow simulations.

Measured metrics include:

* Total simulated operations
* User CPU time
* System CPU time
* CPU utilization
* Total execution time
* Memory consumption

Benchmark results:

| Metric                 | Standard Tor | ZKP-Tor  |
| ---------------------- | ------------ | -------- |
| Operations             | 5000         | 5000     |
| User Time (s)          | 2119.76      | 2089.08  |
| System Time (s)        | 3313.37      | 3197.63  |
| CPU Usage (%)          | 768          | 760      |
| Elapsed Time (mm:ss)   | 11:46.71     | 11:35.20 |
| Elapsed Time (Seconds) | 706.71       | 695.20   |
| Max RAM Used (KB)      | 179612       | 177504   |

The experimental results demonstrate that integrating FFS-based Zero-Knowledge authentication into Tor introduces minimal computational overhead while significantly enhancing exit-node trust and authentication capabilities.

---

# Experimental Environment

* Ubuntu Linux
* Shadow 3.x
* Tor 0.4.8.x
* Large-scale Tor topology
* Multiple clients, relays and exit nodes

---

# Notes

This project is intended for academic and research purposes.

The implementation demonstrates that Zero-Knowledge authentication can be integrated into anonymous communication systems while preserving anonymity properties.

---

# Authors

* Matan Sides
* Ron Haba


