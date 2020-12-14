#!/usr/bin/env python

import contextlib
import os
import glob
import pathlib
import shutil
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class Runner:
    prog_name: str
    source_path: str

    start_time: float = 0
    end_time: float = 0
    variants: List[str] = field(default_factory=list)
    variant: str = ""
    status: int = 0
    # extension: str = field(default="")

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
        cmd = f"{self.variant} {self.source_name}"
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
        # print(self.run_cmd)
        self._run()
        self.end_time = time.time()

    def _run(self):
        self.status = self.system(self.run_cmd)

    def system(self, cmd):
        with chdir("sandbox"):
            return os.system(self.cmd)


class PyRunner(Runner):
    name = "Python"
    extension = "py"
    variants = [
        "python3.6",
        "python3.7",
        "python3.8",
        "python3.9",
        "python3.10",
        "pypy3",
    ]


class LuaRunner(Runner):
    name = "Lua"
    extension = "lua"
    variants = [
        "lua",
        "luajit",
    ]


class JSRunner(Runner):
    name = "JavaScript"
    extension = "js"
    variants = [
        "node",
    ]


class RubyRunner(Runner):
    name = "Ruby"
    extension = "rb"
    variants = [
        "ruby",
    ]


class PhpRunner(Runner):
    name = "PHP"
    extension = "php"
    variants = [
        "php",
    ]


class CythonRunner(Runner):
    name = "Cython"
    extension = "pyx"
    variants = [
        "envs/cython/bin/cython",
        "envs/cython-dev/bin/cython",
        "envs/cython-plus/bin/cython",
    ]

    def compile(self):
        cmd = f"cythonize -3 -bi {self.source_name} > /dev/null"
        os.system(cmd)

    @property
    def run_cmd(self):
        return f"python3.9 -c 'import {self.prog_name}' {self.args} > /dev/null"

    # def _run(self):
    #     # print(self.run_cmd)
    #     self.status = os.system(self.run_cmd)
    #     # sys.exit()


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

        cls = v
        if cls.variants:
            for variant in cls.variants:
                runner = cls(prog_name, source_path, variant=variant)
                runners.append(runner)
        else:
            runner = cls(prog_name, source_path)
            runners.append(runner)

    runners2 = []
    for runner in runners:
        if runner.match():
            runners2.append(runner)

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
                    f"{runner.source_name} {runner.name}/{runner.variant}: {runner.duration}"
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
