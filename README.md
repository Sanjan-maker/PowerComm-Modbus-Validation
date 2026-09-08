# PowerComm – Modbus TCP Simulation & Protocol Validation Framework

> An industrial-inspired Python framework for simulating electrical devices over Modbus TCP and validating communication behaviour through functional, negative, boundary, and performance testing.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Modbus](https://img.shields.io/badge/Protocol-Modbus%20TCP-green)
![Testing](https://img.shields.io/badge/Focus-Protocol%20Validation-orange)
![Status](https://img.shields.io/badge/Status-Learning%20Prototype-success)

---

## Overview

PowerComm is a Python-based engineering prototype designed to explore industrial communication and protocol validation concepts commonly found in power-system monitoring and automation environments.

The project simulates an electrical monitoring device that exposes operating parameters through a Modbus TCP interface. A client application connects to the simulated device, retrieves register values, converts raw register data into engineering values, and validates communication behaviour using structured test scenarios.

The project focuses on the engineering workflow surrounding industrial communication:

- Device simulation
- Modbus TCP communication
- Register mapping
- Client-server interaction
- Raw-to-engineering value conversion
- Functional validation
- Negative testing
- Boundary testing
- Performance measurement
- Communication troubleshooting
- Automated testing

The objective is not to implement a certified industrial device or complete Modbus conformance suite. Instead, this project serves as a learning-oriented engineering prototype demonstrating how industrial communication systems can be simulated and systematically validated.

---

# Problem Statement

Industrial power-system and automation environments rely on communication between field devices, controllers, monitoring systems, and supervisory applications.

A typical workflow involves:

1. A device exposes measurements through communication registers.
2. A client connects to the device.
3. The client reads register values.
4. Raw protocol values are decoded.
5. Values are converted into engineering units.
6. The communication behaviour is validated.
7. Errors and unexpected responses are investigated.

Communication software must therefore be tested not only for successful operation but also for invalid requests, boundary conditions, connection failures, and performance behaviour.

PowerComm was built to explore this validation workflow using a simulated Modbus TCP environment.

---

# Key Features

- Simulated electrical monitoring device
- Modbus TCP server communication
- Modbus TCP client implementation
- Register-based electrical measurements
- Register mapping documentation
- Raw-to-engineering value conversion
- Functional communication testing
- Negative testing
- Boundary testing
- Performance measurement
- Automated testing using Pytest
- Protocol event logging
- Communication troubleshooting workflows
- Modular project architecture

---

# System Architecture

```text
                  ┌─────────────────────────┐
                  │ Electrical Device       │
                  │ Simulator               │
                  └────────────┬────────────┘
                               │
                    Electrical Measurements
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ Modbus Register Map     │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ Modbus TCP Server       │
                  └────────────┬────────────┘
                               │
                         TCP/IP Network
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ Modbus TCP Client       │
                  └────────────┬────────────┘
                               │
                    Raw Register Responses
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ Register Decoder        │
                  └────────────┬────────────┘
                               │
                    Engineering Values
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ Validation Engine       │
                  └────────────┬────────────┘
                               │
             ┌─────────────────┼──────────────────┐
             │                 │                  │
             ▼                 ▼                  ▼
        Functional         Negative           Performance
         Testing           Testing             Testing
