#!/usr/bin/env python3

from plumbum import local
import config

for env in config.ENVS:
    python = env.get("python")
    name = env.get("name", python)
    runner = env.get("runner")
    deps = env.get("deps")

    print(f"Creating env {name}...")

    if python:
        local[python]["-m", "venv", "--copies", "--clear", f"envs/{name}"]()
    else:
        local["python3.8"]["-m", "venv", "--copies", "--clear", f"envs/{name}"]()

    local[f"envs/{name}/bin/pip"]["install", "-U", "pip", "wheel", "setuptools"]()

    if deps:
        local[f"envs/{name}/bin/pip"]["install", deps]()

    if runner != "Cython":
        local[f"envs/{name}/bin/python"]["-m", "pip", "install", "numpy"]()
        local[f"envs/{name}/bin/python"]["-m", "pip", "install", "llvmlite"]()
        local[f"envs/{name}/bin/python"]["-m", "pip", "install", "numba"]()
