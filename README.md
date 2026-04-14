# Experiment Launcher
## Description

This repository contains helper classes and script to launch your computer science experiments from yaml configuration files on any device (Local, Slurm clusters) easily.

This repository is highly inspired from Hydra but is simpler, faster, and customizable for the user with specific needs (see feaures section).

## Install

UV

pyproject.toml
```
pip install "git+https://github.com/quentinletellier/experiment-launcher"
```

PIP

```
uv add "git+https://github.com/quentinletellier/experiment-launcher"
```

## Features

- The launcher command takes a python script and a yaml configuration as input
- Creates a new directory with the current datetime
- Performs a parameter sweep over the provided parameter values and launches a process for each parameter combinations
- Creates an output directory for each process
- Saves a copy of the effective configuration file for each process

## Usage

```
uv run src/experiment_launcher/launch.py --script YOUR_EXP_SCRIPT.py --config YOUR_CONFIG.yaml
```

The given config should have the following structure:

```
# your experiment config
# you are free to write anything you want here

key_1:
    sub_key_1:
        value_1
key_2: value_2
key_3: value_3

# The launcher specific configuration
launcher:
  output_dir: YOUR_OUTPUT_DIR
  sweep:
    key_1.sub_key_1: [option_1, option_2, option_3]
    key_3: [option_1, option_2]
  device_launcher:
    device: slurm # "slurm" or "local"
    # slurm specific configuration
    job-name: YOUR_JOB_NAME
    cpus-per-task: 24
    gpus-per-node: 4
    ...

```

A complete yaml configuration file example is provided at 'example/config.yaml'