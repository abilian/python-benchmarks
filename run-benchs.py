#!/usr/bin/env python

from __future__ import annotations

import contextlib
import glob
import os
import pathlib
import shutil
import subprocess
import time
from dataclasses import dataclass, Field
from typing import List, Dict, Any, Optional

PATH = os.environ["PATH"]


class Runner:
    name: str
    extension: str
    interpreter: str
    variants: List[Dict[str, Any]] = ()

    def match(self, source_name):
        return source_name.endswith(f".{self.extension}")

    def run_all(self, source_path):
        self.prepare_sandbox(source_path)
        if self.variants:
            for variant in self.variants:
                run = Run(self, source_path, variant=variant)
                self.run(run)

        else:
            run = Run(self, source_path)
            self.run(run)

    def prepare_sandbox(self, filename):
        shutil.rmtree("sandbox")
        os.mkdir("sandbox")
        shutil.copy(filename, "sandbox")

    def run(self, run: Run) -> None:
        self.compile(run)
        cmd = self.run_cmd(run)
        run.run(cmd)

    def compile(self, source_name):
        pass

    def run_cmd(self, run: Run) -> List[str]:
        """Default run command.

        Can be overridden in subclass.
        """
        variant = run.variant
        if variant and "interpreter" in variant:
            interpreter = variant["interpreter"]
        else:
            interpreter = self.interpreter

        cmd = [interpreter, run.source_name]
        if run.args:
            cmd += run.args.split(" ")

        return cmd


@dataclass
class Run:
    runner: Runner
    source_path: str
    variant: Optional[Dict] = None
    start_time: float = 0
    end_time: float = 0
    returncode: int = 0

    @property
    def prog_name(self) -> str:
        return pathlib.Path(self.source_path).parent.name

    @property
    def source_name(self) -> str:
        return pathlib.Path(self.source_path).name

    @property
    def variant_name(self) -> str:
        if not self.variant:
            return self.runner.interpreter
        if "virtualenv" in self.variant:
            return self.variant["virtualenv"]
        if "interpreter" in self.variant:
            return self.variant["interpreter"]
        return "???"

    @property
    def virtualenv(self) -> str:
        if self.variant and "virtualenv" in self.variant:
            return self.variant["virtualenv"]
        return ""

    @property
    def args(self) -> str:
        source_dir = pathlib.Path(self.source_path).parent
        args_txt = source_dir / "args.txt"
        if args_txt.exists():
            return args_txt.open().read().strip()
        else:
            return ""

    def run(self, cmd):
        self.start_time = time.time()

        if self.virtualenv:
            # env = dict(os.environ)
            # path = f"{os.getcwd()}/envs/{self.virtualenv}/bin:{PATH}"
            # env["PATH"] = path
            cmd[0] = f"{os.getcwd()}/envs/{self.virtualenv}/bin/{cmd[0]}"
            print(cmd)
            p = subprocess.run(
                cmd,
                cwd="sandbox",
                # env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            print(cmd)
            p = subprocess.run(
                cmd, cwd="sandbox", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

        self.returncode = p.returncode
        self.end_time = time.time()
        self.report()

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

    def report(self):
        print(
            f"{self.source_name:<15} "
            f"{(self.runner.name + '/' + self.variant_name):<20} "
            f"{self.duration:3.3f}"
        )


class PyRunner(Runner):
    name = "Python"
    extension = "py"
    variants = [
        {
            "interpreter": "python3.7",
            "virtualenv": "python3.7",
        },
        {
            "interpreter": "python3.8",
            "virtualenv": "python3.8",
        },
        # {
        #     "interpreter": "python3.9",
        #     "virtualenv": "python3.9",
        # },
        # {
        #     "interpreter": "python3.10",
        # },
        {
            "interpreter": "pypy3",
        },
    ]


class LuaRunner(Runner):
    name = "Lua"
    extension = "lua"
    variants = [
        {"interpreter": "lua"},
        {"interpreter": "luajit"},
    ]


class JSRunner(Runner):
    name = "JavaScript"
    extension = "js"
    interpreter = "node"


class RubyRunner(Runner):
    name = "Ruby"
    extension = "rb"
    interpreter = "ruby"


class PhpRunner(Runner):
    name = "PHP"
    extension = "php"
    interpreter = "php"


class CythonRunner(Runner):
    name = "Cython"
    extension = "pyx"
    variants = [
        {
            "virtualenv": "cython",
        },
        {
            "virtualenv": "cython-dev",
        },
        {
            "virtualenv": "cython-plus",
        },
    ]

    def compile(self, run: Run):
        executable = f"{os.getcwd()}/envs/{run.virtualenv}/bin/cythonize"
        cmd = [executable, "-3", "-bi", run.source_name]
        p = subprocess.run(cmd, cwd="sandbox", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        assert p.returncode == 0

    def run_cmd(self, run: Run) -> List[str]:
        return ["python3", "-c", f"import {run.prog_name}", run.args]


# class CRunner(Runner):
#     name = "C"
#     extension = "c"
#
#     def compile(self):
#         cmd = f"gcc -O {self.file_name}"
#         os.system(cmd)
#
#     @property
#     def run_cmd(self):
#         return f"./a.out {self.args} > /dev/null"


def all_runners():
    def is_runner_subclass(v):
        if not type(v) == type:
            return False
        if v is Runner:
            return False
        if not issubclass(v, Runner):
            return False
        return True

    result = [r() for r in globals().values() if is_runner_subclass(r)]
    return sorted(result, key=lambda x: x.name)


def run_all(prog_name):
    runners = all_runners()

    for source_path in sorted(glob.glob(f"programs/{prog_name}/{prog_name}*")):
        for runner in runners:
            if not runner.match(source_path):
                continue

            runner.run_all(source_path)


@contextlib.contextmanager
def chdir(dirname=None):
    curdir = os.getcwd()
    try:
        if dirname is not None:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(curdir)


def main():
    for program_dir in sorted(glob.glob("programs/*")):
        prog_name = program_dir.split("/")[1]

        # if prog_name != "richards":
        #     continue

        title = f"Running benchmarks for {prog_name}"
        print(title)
        print("=" * len(title))
        print()
        run_all(prog_name)

        print()


if __name__ == "__main__":
    main()
