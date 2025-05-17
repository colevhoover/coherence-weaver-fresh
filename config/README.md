# Configuration

This directory contains configuration files for the Coherence Weaver system.

## Purpose

Configuration files in this directory manage various aspects of the system, such as:

- Agent parameters and settings
- Model configurations
- Environment variables
- Service connection details
- Logging settings
- Workflow parameters

## Usage

Configuration files should use standard formats (JSON, YAML, or INI) and be loaded at runtime by the application.

Example:
```python
import json
from pathlib import Path

# Load a configuration file
config_path = Path(__file__).parent.parent / "config" / "agent_config.json"
with open(config_path, "r") as f:
    config = json.load(f)

# Use the configuration
model_name = config["model_settings"]["model_name"]
```

## Structure

Configuration files should be organized by component or subsystem, with clear naming conventions that indicate their purpose.

## Default Configurations

It's recommended to include default configuration files that can be used as templates or fallbacks if custom configurations are not provided.
