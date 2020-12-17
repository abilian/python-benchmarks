#!/usr/bin/env python3
import os
from dataclasses import dataclass

from plumbum import local
import config


@dataclass
class VirtualEnv:
    python: str = ""
    name: str = ""
    runner: str = ""
    deps: str = ""
    cmd: str = ""

    def __post_init__(self):
        if not self.name:
            self.name = self.python


def create_env(venv: VirtualEnv):
    name = venv.name

    print(f"Creating env {name}...")

    if venv.cmd:
        os.system(venv.cmd)
    elif venv.python:
        local[venv.python]["-m", "venv", "--copies", "--clear", f"envs/{name}"]()
    else:
        local["python3.8"]["-m", "venv", "--copies", "--clear", f"envs/{name}"]()

    local[f"envs/{name}/bin/pip"]["install", "-U", "pip", "wheel", "setuptools"]()


def install_deps(venv: VirtualEnv):
    name = venv.name
    deps = venv.deps
    runner = venv.runner

    print("Installing deps")

    if deps:
        local[f"envs/{name}/bin/pip"]["install", deps]()

    if runner != "Cython":
        local[f"envs/{name}/bin/python"]["-m", "pip", "install", "numpy"]()
        local[f"envs/{name}/bin/python"]["-m", "pip", "install", "llvmlite"]()
        local[f"envs/{name}/bin/python"]["-m", "pip", "install", "numba"]()


for env in config.ENVS:
    venv = VirtualEnv(**env)
    create_env(venv)
    install_deps(venv)
