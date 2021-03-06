#!/usr/bin/env python3

import os
from dataclasses import dataclass

import fire
from plumbum import local
import config


@dataclass
class VirtualEnv:
    python: str = ""
    name: str = ""
    runner: str = ""
    deps: str = ""
    command: str = ""

    def __post_init__(self):
        if not self.name:
            self.name = self.python


def create_env(venv: VirtualEnv):
    name = venv.name

    print(f"Creating env {name}...")

    if venv.command:
        os.system(venv.command)
    elif venv.python:
        local[venv.python]["-m", "venv", "--copies", f"envs/{name}"]()
    else:
        local["python3.8"]["-m", "venv", "--copies", f"envs/{name}"]()

    if not "numba" in venv.name:
        local[f"envs/{name}/bin/pip"]["install", "-U", "pip", "wheel", "setuptools"]()


def install_deps(venv: VirtualEnv):
    name = venv.name

    print("Installing deps")

    if venv.deps:
        local[f"envs/{name}/bin/pip"]["install", venv.deps]()

    if not "numba" in venv.name:
        local[f"envs/{name}/bin/python"]["-m", "pip", "install", "jinja2"]()

    # if venv.runner != "Cython" and venv.python not in {"python3.9", "python3.10"}:
    #     # local[f"envs/{name}/bin/python"]["-m", "pip", "install", "numpy"]()
    #     # local[f"envs/{name}/bin/python"]["-m", "pip", "install", "llvmlite"]()
    #     # local[f"envs/{name}/bin/python"]["-m", "pip", "install", "numba"]()
    #     local[f"envs/{name}/bin/python"]["-m", "pip", "install", "jinja2"]()


def main(env=""):
    for env_dict in config.ENVS:
        venv = VirtualEnv(**env_dict)
        if env and env != venv.name:
            continue

        create_env(venv)
        install_deps(venv)


if __name__ == "__main__":
    fire.Fire(main)
