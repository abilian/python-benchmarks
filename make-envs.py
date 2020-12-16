#!/usr/bin/env python3

from plumbum import local
import config

for env in config.ENVS:
    print(env)

    python = env.get("python")
    name = env.get("name", python)
    runner = env.get("runner")
    deps = env.get("deps")

    if python:
        local[python]["-m", "venv", "--copies", "--clear", f"envs/{name}"]()
    else:
        local["python3.8"]["-m", "venv", "--copies", "--clear", f"envs/{name}"]()

    if deps:
        local[f"envs/{name}/bin/pip"]["install", deps]()

    if runner != "Cython":
        local[f"envs/{name}/bin/python"]["-m", "pip", "install", "numba"]()
