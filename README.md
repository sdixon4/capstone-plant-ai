# Autonomous, Low-Power AI System for Plant Health Monitoring in Space 

This repository contains simulations, fault injection tools, and behavior modeling code for a senior capstone project focused on ethical, embedded AI in space agriculture systems.

## Overview

The goal of this capstone is to develop a robust, low-power FPGA-based system capable of monitoring plant health autonomously aboard the ISS or other constrained environments. It includes fault detection, explainable AI logging, and multi-sensor fusion to ensure reliability and transparency.

## Folder Structure


##  Features

- Simulates Temp, Moisture, CO₂, and Light sensors over 72 hours
- Injects faults: sensor dropout, noise burst, stuck-at errors
- Flags fallback logic based on threshold rules
- Outputs CSV for logging, dashboard, or XAI analysis
- Designed for integration with watchdogs and ethical override systems

## Requirements

- Python 3.8+
- `numpy`, `pandas`, `matplotlib`, `jupyter`

To install:

```bash
pip install -r requirements.txt

