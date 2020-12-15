#!/usr/bin/env python

from __future__ import annotations

import contextlib
import os
import glob
import pathlib
import shutil
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any

from devtools import debug
from plumbum import local

PATH = os.environ["PATH"]


class Runner:
    name: str
    extension: str
    interpreter: str
    variants: List[Dict[str, Any]] = []

    def match(self, source_name):
        return source_name.endswith(f".{self.extension}")

    def prepare_sandbox(self, filename):
        shutil.rmtree("sandbox")
        os.mkdir("sandbox")
        shutil.copy(filename, "sandbox")

    def run_all(self, source_path):
        if self.variants:
            # TODO: multiples axes
            d = self.variants[0]

            if "path" in d:
                for path in d["path"]:
                    run = Run(self, source_path, path=path)
                    self.run(run)

            elif "interpreter" in d:
                for interpreter in d["interpreter"]:
                    run = Run(self, source_path, interpreter=interpreter)
                    self.run(run)

        else:
            run = Run(self, source_path)
            self.run(run)

    def compile(self, source_name: str) -> None:
        pass

    def run(self, run: Run) -> None:
        run.start()
        self._run(run)
        run.stop()
        run.report()

    def _run(self, run: Run) -> None:
        with chdir("sandbox"):
            with local.env(PATH=run.path or PATH):
                cmd = self.run_cmd(run).split(" ")
                print(f"> {cmd}")
                local["sh"]["-c", cmd]()
                # self.status = self.system(self.run_cmd)

    def run_cmd(self, run: Run) -> str:
        """Default run command.

        Can be overridden in subclass.
        """
        cmd = f"{run.interpreter} {run.source_name}"
        if run.args:
            cmd += " " + run.args
        cmd += " > /dev/null"
        return cmd

    # def system(self, cmd: str) -> int:
    #     with chdir("sandbox"):
    #         print(f"> {cmd}")
    #         return os.system(cmd)


@dataclass
class Run:
    runner: Runner
    source_path: str
    interpreter: str = ""
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
    def args(self) -> str:
        source_dir = pathlib.Path(self.source_path).parent
        args_txt = source_dir / "args.txt"
        if args_txt.exists():
            return args_txt.open().read()
        else:
            return ""

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

    def report(self):
        if self.status == 0:
            print(
                f"{self.source_name} {self.runner.name}/{self.interpreter}: {self.duration}"
            )


class PyRunner(Runner):
    name = "Python"
    extension = "py"
    variants = [
        {
            "interpreter": [
                "python3.6",
                "python3.7",
                "python3.8",
                "python3.8",
                "python3.10",
                "pypy3",
            ]
        },
    ]


class LuaRunner(Runner):
    name = "Lua"
    extension = "lua"
    variants = [
        {"interpreter": ["lua", "luajit"]},
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
            "path": [
                f"envs/cython/bin:{PATH}",
                f"envs/cython-dev/bin:{PATH}",
                f"envs/cython-plus/bin:{PATH}",
            ]
        },
    ]

    # def __post_init__(self):
    #     self.name = "Cython"
    #     self.extension = "pyx"
    #     self.variants = [
    #         {
    #             "path": [
    #                 f"envs/cython/bin:{PATH}",
    #                 f"envs/cython-dev/bin:{PATH}",
    #                 f"envs/cython-plus/bin:{PATH}",
    #             ]
    #         },
    #     ]

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

    # runners = []
    # ns = globals()
    # for v in ns.values():
    #     if not is_runner_subclass(v):
    #         continue
    #
    #     debug(v)
    #     cls = v
    #     if cls.variants:
    #         # TODO: multiples axes
    #         d = cls.variants[0]
    #
    #         if "path" in d:
    #             for path in d["path"]:
    #                 runner = cls(path=path)
    #                 runners.append(runner)
    #
    #         elif "interpreter" in d:
    #             for interpreter in d["interpreter"]:
    #                 runner = cls(interpreter=interpreter)
    #                 runners.append(runner)
    #
    #     else:
    #         runner = cls()
    #         runners.append(runner)
    #
    # return runners

    # # debug(runners)
    #
    # runners2 = []
    # for runner in runners:
    #     if runner.match():
    #         runners2.append(runner)
    #
    # debug(runners2)
    #
    # return runners2


def run_all(prog_name):
    runners = all_runners()

    for source_path in glob.glob(f"programs/{prog_name}/{prog_name}*"):
        for runner in runners:
            if not runner.match(source_path):
                continue

            print(f"Running runner {runner.name} on {source_path}")

            runner.run_all(source_path)

            # runner.prepare_sandbox(source_path)
            # runner.compile(source_path)
            # runner.run_all(source_path)
            #
            # if runner.status == 0:
            #     print(
            #         f"{runner.source_name} {runner.name}/{runner.intepreter}: {runner.duration}"
            #     )


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
