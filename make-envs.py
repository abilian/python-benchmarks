#!/usr/bin/env python3

import os
import shutil
from dataclasses import dataclass
from pathlib import Path

import fire
import rich
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

    rich.print(f"[bold green]Creating env {name}...[/bold green]")

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

    rich.print(f"[bold green]...Installing deps for {name}[/bold green]")

    if venv.deps:
        local[f"envs/{name}/bin/pip"]["install", venv.deps]()

    if "numba" not in venv.name:
        local[f"envs/{name}/bin/python"]["-m", "pip", "install", "jinja2"]()

    # if venv.runner != "Cython" and venv.python not in {"python3.9", "python3.10"}:
    #     # local[f"envs/{name}/bin/python"]["-m", "pip", "install", "numpy"]()
    #     # local[f"envs/{name}/bin/python"]["-m", "pip", "install", "llvmlite"]()
    #     # local[f"envs/{name}/bin/python"]["-m", "pip", "install", "numba"]()
    #     local[f"envs/{name}/bin/python"]["-m", "pip", "install", "jinja2"]()


def destroy_env(venv: VirtualEnv):
    name = venv.name
    rich.print("[bold red]Something went wrong, destroying env[/bold red]")
    rm_rf(f"envs/{name}")


def rm_rf(path: str):
    if Path(path).exists():
        shutil.rmtree(path)


def make_env(venv):
    try:
        create_env(venv)
        install_deps(venv)
        print()
    except:
        destroy_env(venv)


def main(env=""):
    for env_dict in config.ENVS:
        venv = VirtualEnv(**env_dict)
        if env and env != venv.name:
            continue

        if Path(f"envs/{venv.name}").exists():
            rich.print(f"[cyan]Env {venv.name} already exists, skipping[/cyan]")
            continue

        make_env(venv)


if __name__ == "__main__":
    fire.Fire(main)
