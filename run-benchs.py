#!/usr/bin/env python

from __future__ import annotations

import contextlib
import glob
import os
import pathlib
import shutil
import time
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from plumbum import local

PATH = os.environ["PATH"]


class Runner:
    name: str
    extension: str
    interpreter: str
    variants: List[Dict[str, Any]] = []

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

    def compile(self, source_name: str) -> None:
        pass

    def run(self, run: Run) -> None:
        cmd = self.run_cmd(run)
        run.run(cmd)

    def run_cmd(self, run: Run) -> str:
        """Default run command.

        Can be overridden in subclass.
        """
        variant = run.variant
        if variant and "interpreter" in variant:
            interpreter = variant["interpreter"]
        else:
            interpreter = self.interpreter

        cmd = f"{interpreter} {run.source_name}"
        if run.args:
            cmd += " " + run.args

        return cmd


@dataclass
class Run:
    runner: Runner
    source_path: str
    variant: Optional[Dict] = None
    start_time: float = 0
    end_time: float = 0
    status: int = 0
    path: str = ""

    @property
    def prog_name(self) -> str:
        return pathlib.Path(self.source_path).parent.name

    @property
    def source_name(self) -> str:
        return pathlib.Path(self.source_path).name

    @property
    def variant_name(self) -> str:
        if not self.variant:
            return ""
        if "env" in self.variant:
            return self.variant["env"]
        if "interpreter" in self.variant:
            return self.variant["interpreter"]

    @property
    def args(self) -> str:
        source_dir = pathlib.Path(self.source_path).parent
        args_txt = source_dir / "args.txt"
        if args_txt.exists():
            return args_txt.open().read()
        else:
            return ""

    def run(self, cmd):
        self.start_time = time.time()

        with chdir("sandbox"):
            with local.env(PATH=self.path or PATH):
                # print(f"> {cmd}")
                local["sh"]["-c", cmd]()

        self.end_time = time.time()
        self.report()

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

    def report(self):
        if self.status == 0:
            print(
                f"{self.source_name} {self.runner.name}/{self.variant}: {self.duration}"
            )


class PyRunner(Runner):
    name = "Python"
    extension = "py"
    variants = [
        {
            "interpreter": "python3.6",
        },
        {
            "interpreter": "python3.7",
        },
        {
            "interpreter": "python3.8",
        },
        {
            "interpreter": "python3.8",
        },
        {
            "interpreter": "python3.10",
        },
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
            "name": "cython",
            "virtualenv": "cython",
        },
        {
            "name": "cython-dev",
            "virtualenv": "cython-dev",
        },
        {
            "name": "cython-dev",
            "virtualenv": "cython-dev",
        },
        #
        #     "path": [
        #         f"envs/cython/bin:{PATH}",
        #         f"envs/cython-dev/bin:{PATH}",
        #         f"envs/cython-plus/bin:{PATH}",
        #     ]
        # },
    ]

    def compile(self, run: Run):
        with local.env(PATH=run.path):
            local.cythonize["-3", "-bi", run.source_name]()
            # cmd = f"cythonize -3 -bi {self.source_name} > /dev/null"
            # os.system(cmd)

    def run_cmd(self, run: Run) -> str:
        return f"python3.8 -c 'import {run.prog_name}' {run.args} > /dev/null"


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

    return [r() for r in globals().values() if is_runner_subclass(r)]


def run_all(prog_name):
    runners = all_runners()

    for source_path in glob.glob(f"programs/{prog_name}/{prog_name}*"):
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
    for program_dir in glob.glob("programs/*"):
        prog_name = program_dir.split("/")[1]
        if prog_name != "richards":
            continue

        title = f"Running benchmarks for {prog_name}"
        print(title)
        print("=" * len(title))
        print()
        run_all(prog_name)

        print()


if __name__ == "__main__":
    main()
