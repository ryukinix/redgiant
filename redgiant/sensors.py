"""
Read temperature of CPU and GPU.
"""

import subprocess
import json

cpu_sensor = "coretemp-isa-0000"


def _get_input_temp_field_name(cpu_data: dict) -> str:
    for field in cpu_data:
        if "input" in field:
            return field
    raise ValueError(f"Not input field found for {cpu_data}")


def get_cpu_temperature() -> float:
    cmd = ["sensors", "-j"]
    output = subprocess.check_output(cmd)
    parsed = json.loads(output)

    cpu_fields = parsed[cpu_sensor]
    cpu_temperatures = []
    for field in cpu_fields:
        if field.lower().startswith("core"):
            cpu_data = cpu_fields[field]
            cpu_temperature_field = _get_input_temp_field_name(cpu_data)
            cpu_temperatures.append(cpu_data[cpu_temperature_field])

    return sum(cpu_temperatures) / len(cpu_temperatures)


def get_gpu_temperature() -> float:
    cmd = ["nvidia-smi",
           "--query-gpu=temperature.gpu",
           "--format=csv,noheader,nounits"]
    output = subprocess.check_output(cmd)
    parsed = float(output.strip())
    return parsed
