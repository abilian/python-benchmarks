#!/usr/bin/env python

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


@dataclass
class Runner:
    prog_name: str
    source_path: str

    start_time: float = 0
    end_time: float = 0
    variants: List[Dict[str, Any]] = field(default_factory=list)
    interpreter: str = ""
    status: int = 0
    path: str = ""
    extension: str = ""

    @property
    def source_name(self):
        return pathlib.Path(self.source_path).name

    @property
    def duration(self):
        return self.end_time - self.start_time

    @property
    def args(self):
        if Path("args.txt").exists():
            return open("args.txt").read()
        else:
            return ""

    @property
    def run_cmd(self):
        cmd = f"{self.interpreter} {self.source_name}"
        if self.args:
            cmd += " " + self.args
        cmd += " > /dev/null"
        return cmd

    def match(self):
        return self.source_name.endswith(f".{self.extension}")

    def compile(self):
        pass

    def run(self):
        self.start_time = time.time()
        self._run()
        self.end_time = time.time()

    def _run(self):
        with local.env(PATH=self.path or PATH):
            cmd = self.run_cmd.split(" ")
            local["sh"]["-c", cmd]()
            # self.status = self.system(self.run_cmd)

    def system(self, cmd):
        with chdir("sandbox"):
            print(f"> {cmd}")
            return os.system(cmd)


class PyRunner(Runner):
    def __post_init__(self):
        self.name = "Python"
        self.extension = "py"
        self.variants = [
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
    def __post_init__(self):
        self.name = "Lua"
        self.extension = "lua"
        self.variants = [
            {"interpreter": ["lua", "luajit"]},
        ]
        debug(vars(self))


class JSRunner(Runner):
    def __post_init__(self):
        self.name: str = "JavaScript"
        self.extension: str = "js"
        self.interpreter: str = "node"
        debug(vars(self))


class RubyRunner(Runner):
    def __post_init__(self):
        self.name = "Ruby"
        self.extension = "rb"
        self.interpreter = "ruby"
        debug(vars(self))


class PhpRunner(Runner):
    def __post_init__(self):
        self.name = "PHP"
        self.extension = "php"
        self.interpreter = "php"
        debug(vars(self))


class CythonRunner(Runner):
    def __post_init__(self):
        self.name = "Cython"
        self.extension = "pyx"
        self.variants = [
            {
                "path": [
                    f"envs/cython/bin:{PATH}",
                    f"envs/cython-dev/bin:{PATH}",
                    f"envs/cython-plus/bin:{PATH}",
                ]
            },
        ]
        debug(vars(self))

    def compile(self):
        with local.env(PATH=self.path):
            local.cythonize["-3", "-bi", self.source_name]()
            # cmd = f"cythonize -3 -bi {self.source_name} > /dev/null"
            # os.system(cmd)

    @property
    def run_cmd(self):
        return f"python3.8 -c 'import {self.prog_name}' {self.args} > /dev/null"


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


def get_runners(prog_name, source_path):
    runners = []
    ns = globals()
    for v in ns.values():
        if not is_runner_subclass(v):
            continue

        debug(v)
        cls = v
        if cls.variants:
            # TODO: multiples axes
            d = cls.variants[0]

            if "path" in d:
                for path in d["path"]:
                    runner = cls(prog_name, source_path, path=path)
                    runners.append(runner)

            elif "interpreter" in d:
                for interpreter in d["interpreter"]:
                    runner = cls(prog_name, source_path, interpreter=interpreter)
                    runners.append(runner)

        else:
            runner = cls(prog_name, source_path)
            runners.append(runner)

    # debug(runners)

    runners2 = []
    for runner in runners:
        if runner.match():
            runners2.append(runner)

    debug(runners2)

    return runners2


def is_runner_subclass(v):
    if not type(v) == type:
        return False
    if v is Runner:
        return False
    if not issubclass(v, Runner):
        return False
    return True


def prepare_sandbox(filename):
    shutil.rmtree("sandbox")
    os.mkdir("sandbox")
    shutil.copy(filename, "sandbox")


def run_all(prog_name):
    for source_path in glob.glob(f"programs/{prog_name}/{prog_name}*"):
        for runner in get_runners(prog_name, source_path):
            prepare_sandbox(source_path)
            runner.compile()
            runner.run()
            if runner.status == 0:
                print(
                    f"{runner.source_name} {runner.name}/{runner.intepreter}: {runner.duration}"
                )


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
